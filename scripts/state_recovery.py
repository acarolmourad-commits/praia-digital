"""Supervised recovery protocol. Requires a trusted external evidence adapter.

No production adapter or automatic retry is supplied. Never derives proof from PID/age.
"""
import hashlib
import json
import os
from pathlib import Path
import time
import re
import uuid

from delivery_journal import ReconciliationRequired, atomic_text, digest
from state_store import locked, validate, checked_path


def fingerprint(value):
    return digest(json.dumps(value, sort_keys=True))


class Recovery:
    def __init__(self, root, expected, verifier):
        self.root = checked_path(root)
        self.expected = expected
        self.verifier = verifier  # Privileged supervisor/provider adapter, not user JSON.

    def read_audit(self, path):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            raise ReconciliationRequired('Invalid authoritative audit; preserve for supervised repair') from None
        manifest = validate(self.root, self.expected)
        if not isinstance(data, dict) or not isinstance(data.get('report'), dict):
            raise ReconciliationRequired('Invalid audit shape')
        report = data['report']
        if (data.get('schema') != 3 or data.get('phase') not in ('PREPARED', 'COMPLETE') or
                report.get('state_id') != manifest['state_id'] or report.get('identity') != self.expected or
                data.get('digest') != fingerprint(report) or
                path.name != 'recovery-' + data['digest'] + '.json'):
            raise ReconciliationRequired('Audit integrity or identity mismatch')
        self.check_records(report)
        if data['phase'] == 'COMPLETE' and report['run'] is not None:
            archive = self.root / ('run-' + data['digest'] + '.archived.json')
            if not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest() != report['run_hash']:
                raise ReconciliationRequired('Completed recovery archive missing or changed')
        return data

    def check_records(self, report):
        for entry in report['attempts']:
            name = entry['file']
            if Path(name).name != name or not name.endswith('.attempt.json'):
                raise ReconciliationRequired('Invalid attempt path in audit')
            path = checked_path(self.root / name)
            if hashlib.sha256(path.read_bytes()).hexdigest() != entry['hash']:
                raise ReconciliationRequired('Attempt changed since reconciliation')

    def resolved(self):
        resolved = set()
        for path in self.root.glob('recovery-*.json'):
            data = self.read_audit(path)
            if data['phase'] == 'PREPARED':
                raise ReconciliationRequired('Resume approved recovery before preparing another')
            resolved.update(entry['file'] for entry in data['report']['attempts'])
        return resolved

    def inspect(self):
        manifest = validate(self.root, self.expected)
        marker = self.root / 'run.pending.json'
        run = json.loads(marker.read_text()) if marker.exists() else None
        resolved = self.resolved()
        attempts = []
        for p in sorted(self.root.glob('*.attempt.json')):
            record = json.loads(p.read_text())
            if p.name in resolved or record.get('status') == 'CSV_COMMITTED':
                continue
            if (record.get('version') != 2 or record.get('state_id') != manifest['state_id'] or
                    record.get('identity_hash') != fingerprint(self.expected)):
                raise ReconciliationRequired('Attempt identity mismatch; preserve evidence')
            attempts.append((p, record))
        if not attempts and run is None:
            raise ReconciliationRequired('Nothing pending')
        # Adapter must retain handles for the full managed process tree; a missing
        # supervisor record is not equivalent to an empty/dead tree.
        handles = self.verifier.process_handles()
        if not handles or not self.verifier.tree_is_complete():
            raise ReconciliationRequired('Complete retained process tree unavailable')
        pids = set()
        for process in handles:
            if process.pid is None or process.exitcode is None or process.is_alive():
                raise ReconciliationRequired('Managed process still alive or identity unavailable')
            pids.add(process.pid)
        owners = {r['owner_pid'] for _, r in attempts}
        if run:
            if run.get('state_id') != manifest['state_id']:
                raise ReconciliationRequired('Run identity mismatch')
            owners.add(run['pid'])
        if not owners.issubset(pids):
            raise ReconciliationRequired('Owner handle missing')
        resource = checked_path(self.expected['resource'])
        observations = []
        for path, record in attempts:
            evidence = self.verifier.observe(self.expected, record)
            # Expected adapter must query an authoritative destination, never infer
            # NOT_DELIVERED from timeout, absence in a partial listing, or exit status.
            required = {'account': self.expected['account'], 'attempt_id': record['attempt_id'],
                        'recipient_hash': record['recipient_hash'], 'message_hash': record['message_hash']}
            if any(evidence.get(k) != v for k, v in required.items()) or not evidence.get('evidence_id'):
                raise ReconciliationRequired('Proof not bound to account/attempt/payload')
            if evidence.get('outcome') not in ('DELIVERED', 'NOT_DELIVERED'):
                raise ReconciliationRequired('Remote outcome unknown')
            if evidence['outcome'] == 'DELIVERED' and not evidence.get('receipt_id'):
                raise ReconciliationRequired('Delivery proof requires a remote receipt')
            if record.get('receipt_id') and evidence.get('receipt_id') != record['receipt_id']:
                raise ReconciliationRequired('Receipt mismatch')
            if not self.verifier.local_reconciled(resource, record, evidence):
                raise ReconciliationRequired('Local business state not reconciled')
            observations.append({'file': path.name, 'hash': hashlib.sha256(path.read_bytes()).hexdigest(),
                                 'evidence': evidence})
        resource_proof = self.verifier.resource_snapshot(resource)
        # Includes Git integrity/publication checks in adapters for repository resources.
        if not resource_proof or resource_proof.get('publication') != 'RECONCILED':
            raise ReconciliationRequired('Publication/local resource proof incomplete')
        return {'state_id': manifest['state_id'], 'identity': self.expected,
                'run': run, 'run_hash': hashlib.sha256(marker.read_bytes()).hexdigest() if run else None, 'attempts': observations, 'resource': resource_proof,
                'processes': sorted(pids)}

    def prepare(self):
        with locked(self.root, self.expected, 'run'), locked(self.root, self.expected, 'delivery'):
            report = self.inspect()
            return fingerprint(report), report

    def persist(self, audit, data):
        # Partial bytes are evidence, not authority. Preserve failures; never truncate
        # the existing PREPARED audit or let a partial file block a safe retry.
        partial = self.root / ('.recovery-' + data['digest'] + '-' + uuid.uuid4().hex[:8] + '.partial')
        with partial.open('x', encoding='utf-8') as stream:
            json.dump(data, stream, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        # Parse and validate exactly what will become authoritative after replace.
        saved = json.loads(partial.read_text(encoding='utf-8'))
        if saved != data or saved['digest'] != fingerprint(saved['report']):
            raise ReconciliationRequired('Partial audit validation failed; evidence retained')
        os.replace(partial, audit)

    def partial_evidence(self, approved_digest):
        # Classify remnants for the durable audit. Invalid/truncated files remain
        # untouched and cannot certify reconciliation. Fresh inspection is required
        # before the first PREPARED audit, even if a complete partial JSON exists.
        evidence = []
        for path in sorted(self.root.glob('.recovery-' + approved_digest + '-*.partial')):
            raw = path.read_bytes()
            valid = False
            try:
                data = json.loads(raw)
                valid = (isinstance(data, dict) and data.get('schema') == 3 and
                         data.get('digest') == approved_digest and
                         data.get('phase') in ('PREPARED', 'COMPLETE') and
                         fingerprint(data.get('report')) == approved_digest and
                         data['report'].get('identity') == self.expected)
            except (ValueError, TypeError, KeyError):
                pass
            evidence.append({'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(),
                             'valid_payload': valid})
        return evidence

    def recheck_prepared(self, report):
        self.check_records(report)
        resource = checked_path(self.expected['resource'])
        if self.verifier.resource_snapshot(resource) != report['resource']:
            raise ReconciliationRequired('Resource changed during recovery; preserve prepared transaction')
        for entry in report['attempts']:
            record = json.loads((self.root / entry['file']).read_text())
            if (self.verifier.observe(self.expected, record) != entry['evidence'] or
                    not self.verifier.local_reconciled(resource, record, entry['evidence'])):
                raise ReconciliationRequired('Remote/local proof changed during recovery')
        # Process-termination proof was durably approved in PREPARED. Runtime
        # writers refuse PREPARED transactions; resumption does not need handles
        # that the supervisor may have retired after the approved termination.

    def archive_run(self, report, approved_digest):
        if report['run'] is None:
            return
        marker = self.root / 'run.pending.json'
        archive = self.root / ('run-' + approved_digest + '.archived.json')
        if archive.exists():
            if hashlib.sha256(archive.read_bytes()).hexdigest() != report['run_hash'] or marker.exists():
                raise ReconciliationRequired('Conflicting run/archive evidence; no files removed')
            return  # Previous attempt already completed the rename.
        if not marker.exists() or hashlib.sha256(marker.read_bytes()).hexdigest() != report['run_hash']:
            raise ReconciliationRequired('Run marker changed; do not archive another run')
        marker.rename(archive)

    def approve(self, approved_digest):
        if not isinstance(approved_digest, str) or not re.fullmatch('[0-9a-f]{64}', approved_digest):
            raise ReconciliationRequired('Explicit valid approval digest required')
        with locked(self.root, self.expected, 'run'), locked(self.root, self.expected, 'delivery'):
            audit = self.root / ('recovery-' + approved_digest + '.json')
            if audit.exists():
                data = self.read_audit(audit)
                if data['phase'] == 'COMPLETE':
                    return audit  # Idempotent acknowledgement, never touches a newer run.
            else:
                report = self.inspect()
                if fingerprint(report) != approved_digest:
                    raise ReconciliationRequired('Evidence changed since review')
                data = {'schema': 3, 'phase': 'PREPARED', 'digest': approved_digest,
                        'report': report, 'approved_at': time.time(),
                        'prior_partials': self.partial_evidence(approved_digest)}
                self.persist(audit, data)
            self.recheck_prepared(data['report'])
            self.archive_run(data['report'], approved_digest)
            complete = dict(data, phase='COMPLETE', completed_at=time.time(),
                            prior_partials=self.partial_evidence(approved_digest))
            self.persist(audit, complete)
            # Attempt files are unchanged. COMPLETE excludes them from future
            # recovery ownership checks, but delivery_journal still blocks resend.
            return audit

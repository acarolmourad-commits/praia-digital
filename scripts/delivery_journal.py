"""Conservative local write-ahead journal; never retries an attempted delivery."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import uuid
from state_store import locked, validate, StateRefused, assert_recovery_idle


class ReconciliationRequired(RuntimeError):
    pass


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


@contextmanager
def atomic_text(path, **kwargs):
    path = Path(path)
    fd, temporary = tempfile.mkstemp(prefix='.write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', **kwargs) as stream:
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def exclusive_json(path, value):
    # On interrupted/failed persistence, a partial file still blocks retry.
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, sort_keys=True)
        stream.flush()
        os.fsync(stream.fileno())


def replace_json(path, value):
    with atomic_text(path) as stream:
        json.dump(value, stream, sort_keys=True)


@contextmanager
def run_guard(root, expected):
    root = Path(root)
    with locked(root, expected, 'run'):
        assert_recovery_idle(root, expected)
        marker = root / 'run.pending.json'
        owner = {'pid': os.getpid(), 'status': 'RUNNING', 'run_id': uuid.uuid4().hex,
                 'started': time.time(), 'state_id': validate(root, expected)['state_id']}
        try:
            exclusive_json(marker, owner)
        except FileExistsError:
            raise ReconciliationRequired('Interrupted run; supervised reconciliation required') from None
        try:
            yield
        except BaseException:
            raise
        else:
            if json.loads(marker.read_text(encoding='utf-8')) != owner:
                raise ReconciliationRequired('Run marker changed; not removed')
            marker.unlink()


def attempt_path(root, lead, stage):
    return Path(root) / (digest(json.dumps([str(lead), stage])) + '.attempt.json')


def blocked(root, lead, stage):
    if attempt_path(root, lead, stage).exists():
        return True
    for p in Path(root).glob('*.attempt.json'):
        if p.name == 'run.pending.json':
            continue
        try:
            record = json.loads(p.read_text(encoding='utf-8'))
        except (ValueError, OSError):
            return True
        if not isinstance(record, dict) or not isinstance(record.get('lead_hash'), str):
            return True
        if record['lead_hash'] != digest(str(lead)):
            continue
        if record.get('status') != 'CSV_COMMITTED':
            return True
    return False


def send_once(root, lead, stage, recipient, text, transport, confirmed, expected):
    with locked(root, expected, 'delivery'):
        assert_recovery_idle(root, expected)
        return _send_once(Path(root), lead, stage, recipient, text, transport, confirmed, expected)


def _send_once(root, lead, stage, recipient, text, transport, confirmed, expected):
    if blocked(root, lead, stage):
        raise ReconciliationRequired('Previous attempt requires reconciliation; not resent')
    path = attempt_path(root, lead, stage)
    record = {'version': 2, 'status': 'INTENT', 'stage': stage, 'lead_hash': digest(str(lead)),
              'owner_pid': os.getpid(), 'attempt_id': uuid.uuid4().hex, 'started': time.time(),
              'state_id': validate(root, expected)['state_id'],
              'identity_hash': digest(json.dumps(expected, sort_keys=True)),
              'recipient_hash': digest(str(recipient)), 'message_hash': digest(text)}
    try:
        exclusive_json(path, record)
    except FileExistsError:
        raise ReconciliationRequired('Attempt already claimed; not resent') from None
    # No side effect until durable local intent. Never erase intent on failure.
    try:
        stdout, rc = transport(recipient, text)
        receipt = confirmed(stdout, rc)
        accepted = isinstance(receipt, str) and bool(receipt.strip())
    except Exception:
        record['status'] = 'UNCERTAIN'
        replace_json(path, record)
        raise ReconciliationRequired('Transport outcome unknown; reconcile before retry') from None
    record['status'] = 'CONFIRMED' if accepted else 'UNCERTAIN'
    record['observed_at'] = time.time()
    if accepted:
        record['receipt_id'] = receipt
    replace_json(path, record)
    if not accepted:
        raise ReconciliationRequired('Receipt not confirmed; reconcile before retry')
    return path


def mark_csv_committed(path, expected):
    with locked(path.parent, expected, 'delivery'):
        assert_recovery_idle(path.parent, expected)
        record = json.loads(path.read_text(encoding='utf-8'))
        if record.get('status') != 'CONFIRMED':
            raise ReconciliationRequired('Unexpected journal state')
        record['status'] = 'CSV_COMMITTED'
        record['local_committed_at'] = time.time()
        replace_json(path, record)

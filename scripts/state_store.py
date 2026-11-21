"""Explicitly provisioned private state, bound to account, resource and directory."""
from contextlib import contextmanager
import json
import msvcrt
import os
from pathlib import Path
import time
import uuid
import hashlib


class StateRefused(RuntimeError):
    pass


def assert_recovery_idle(root, expected):
    for path in Path(root).glob('recovery-*.json'):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            report = data['report']
            valid = (data['schema'] == 3 and report['identity'] == expected and
                     report['state_id'] == validate(root, expected)['state_id'] and
                     data['digest'] == hashlib.sha256(json.dumps(report, sort_keys=True).encode()).hexdigest())
            for entry in report['attempts']:
                name = entry['file']
                if Path(name).name != name or not name.endswith('.attempt.json'):
                    valid = False
                    break
                recorded = checked_path(Path(root) / name)
                valid = valid and hashlib.sha256(recorded.read_bytes()).hexdigest() == entry['hash']
            if data.get('phase') == 'COMPLETE' and report['run'] is not None:
                archived = checked_path(Path(root) / ('run-' + data['digest'] + '.archived.json'))
                valid = valid and hashlib.sha256(archived.read_bytes()).hexdigest() == report['run_hash']
        except (OSError, ValueError, KeyError, TypeError):
            raise StateRefused('Invalid recovery audit; supervised repair required') from None
        if not valid or data.get('phase') != 'COMPLETE':
            raise StateRefused('Approved recovery is incomplete; resume before new work')


def checked_path(value, *, strict=True):
    p = Path(value)
    if not p.is_absolute():
        raise StateRefused('Absolute state/resource path required')
    for part in (p, *p.parents):
        if part.is_symlink() or getattr(part, 'is_junction', lambda: False)():
            raise StateRefused('Symlink/junction in state/resource path')
    return p.resolve(strict=strict)


def identity(provider, account, dataset, resource):
    if any(not isinstance(v, str) or not v.strip() for v in (provider, account, dataset)):
        raise StateRefused('Provider, explicit account and dataset are required')
    return {'provider': provider, 'account': account, 'dataset': dataset,
            'resource': os.path.normcase(str(checked_path(resource)))}


def directory_id(path):
    st = path.stat()
    return [st.st_dev, st.st_ino]


def initialize(root, expected):
    """Provisioning only. Never called by a sender; refuses existing directories."""
    root = checked_path(root, strict=False)
    if root.exists():
        raise StateRefused('Refuse existing state directory; no implicit migration/reset')
    root.mkdir(mode=0o700)  # Parent must already exist and have reviewed ACLs.
    manifest = {'version': 2, 'state_id': uuid.uuid4().hex, 'identity': expected,
                'root': os.path.normcase(str(root)), 'directory_id': directory_id(root)}
    # Write the identity LAST. Partial initialization never authorizes sending.
    for name in ('run.lock', 'delivery.lock'):
        with (root / name).open('xb') as stream:
            stream.write(b'0')
            stream.flush()
            os.fsync(stream.fileno())
    with (root / 'identity.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, sort_keys=True)
        stream.flush()
        os.fsync(stream.fileno())
    return manifest


def validate(root, expected):
    root = checked_path(root)
    try:
        manifest = json.loads((root / 'identity.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        raise StateRefused('State not initialized or identity corrupted') from None
    if (not isinstance(manifest, dict) or manifest.get('version') != 2 or
            manifest.get('identity') != expected or not manifest.get('state_id') or
            manifest.get('root') != os.path.normcase(str(root)) or
            manifest.get('directory_id') != directory_id(root)):
        raise StateRefused('State/account/resource/directory identity mismatch')
    for name in ('identity.json', 'run.lock', 'delivery.lock'):
        p = checked_path(root / name)
        if not p.is_file() or p.stat().st_nlink != 1:
            raise StateRefused('State metadata must be private regular files')
    return manifest


@contextmanager
def locked(root, expected, kind, timeout=0.3):
    if kind not in ('run', 'delivery'):
        raise ValueError('Unknown state lock')
    root = Path(root)
    manifest = validate(root, expected)
    path = root / (kind + '.lock')
    with path.open('r+b', buffering=0) as stream:
        os.set_inheritable(stream.fileno(), False)
        file_id = (os.fstat(stream.fileno()).st_dev, os.fstat(stream.fileno()).st_ino)
        deadline = time.monotonic() + timeout
        while True:
            try:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise StateRefused('State busy; no work performed') from None
                time.sleep(0.01)
        try:
            current = validate(root, expected)
            if current != manifest or directory_id(path) != list(file_id):
                raise StateRefused('State changed while acquiring lock')
            yield current
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
    # Persistent lock files are never deleted, including after process death.

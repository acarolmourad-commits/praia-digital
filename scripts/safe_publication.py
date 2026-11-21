"""Publish only a single generated commit based on the exact approved remote tip."""
import os
from pathlib import Path
import subprocess

EXPECTED_REMOTE = 'https://github.com/acarolmourad-commits/praia-digital.git'


class PublicationRefused(RuntimeError):
    pass


def git(repo, *args, allowed_codes=(0,)):
    # Ambient Git overrides must not redirect the checkout/index/object store/config.
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0',
               GIT_LITERAL_PATHSPECS='1', GIT_NO_REPLACE_OBJECTS='1',
               GIT_ALLOW_PROTOCOL='https:file')
    result = subprocess.run(['git', '-c', 'core.hooksPath=NUL', '-c', 'core.fsmonitor=false',
                             '-c', 'push.gpgSign=false',
                             '-C', str(repo), *args], capture_output=True, text=True, env=env)
    if result.returncode not in allowed_codes:
        # Do not echo remote URLs, credentials, or hook/provider output.
        raise PublicationRefused('Git operation failed: ' + args[0])
    return result.stdout.strip() if '-z' not in args else result.stdout


def validate_identity(repo, expected_remote):
    root = Path(repo).resolve(strict=True)
    actual = Path(git(repo, 'rev-parse', '--show-toplevel')).resolve(strict=True)
    gitdir = Path(git(repo, 'rev-parse', '--absolute-git-dir')).resolve(strict=True)
    common = Path(git(repo, 'rev-parse', '--git-common-dir'))
    if not common.is_absolute():
        common = root / common
    marker = root / '.git'
    if (actual != root or not marker.is_dir() or marker.is_symlink() or
            getattr(marker, 'is_junction', lambda: False)() or
            gitdir != marker.resolve() or common.resolve() != gitdir):
        raise PublicationRefused('Expected standalone checkout root and private Git directory')
    if git(repo, 'symbolic-ref', '--quiet', 'HEAD') != 'refs/heads/main':
        raise PublicationRefused('Publication requires attached main branch')
    for mode in ((), ('--push',)):
        urls = git(repo, 'remote', 'get-url', *mode, '--all', 'origin').splitlines()
        if urls != [expected_remote]:
            raise PublicationRefused('Unexpected origin URL or multiple destinations')
    if git(repo, 'config', '--get-regexp', r'^url\..*\.(insteadof|pushinsteadof)$', allowed_codes=(0, 1)):
        raise PublicationRefused('URL rewrites require manual review')
    for name in ('index.lock', 'HEAD.lock', 'MERGE_HEAD', 'CHERRY_PICK_HEAD',
                 'REVERT_HEAD', 'rebase-merge', 'rebase-apply'):
        p = Path(git(repo, 'rev-parse', '--git-path', name))
        if not p.is_absolute():
            p = Path(repo) / p
        if p.exists():
            raise PublicationRefused('Git operation or lock present')


def remote_tip(repo, expected_remote):
    lines = git(repo, 'ls-remote', '--exit-code', expected_remote, 'refs/heads/main').splitlines()
    if len(lines) != 1 or lines[0].split()[1:] != ['refs/heads/main']:
        raise PublicationRefused('Remote main is ambiguous or missing')
    return lines[0].split()[0]


def begin(repo, expected_remote=EXPECTED_REMOTE):
    validate_identity(repo, expected_remote)
    if git(repo, 'status', '--porcelain', '--untracked-files=all'):
        raise PublicationRefused('Dedicated clean checkout required')
    head = git(repo, 'rev-parse', 'HEAD')
    if head != remote_tip(repo, expected_remote):
        raise PublicationRefused('Local HEAD must equal live remote main; prior commits are not published')
    return head


def publish(repo, base, targets, expected_remote=EXPECTED_REMOTE):
    validate_identity(repo, expected_remote)
    if git(repo, 'rev-parse', 'HEAD') != base or remote_tip(repo, expected_remote) != base:
        raise PublicationRefused('Local or remote HEAD changed during generation')
    targets = set(targets)
    if not targets or any(Path(p).is_absolute() or '..' in Path(p).parts or
                          '.git' in Path(p).parts for p in targets):
        raise PublicationRefused('Invalid publication paths')
    changed = set()
    for args in (('diff', '--name-only', '-z'), ('diff', '--cached', '--name-only', '-z'),
                 ('ls-files', '--others', '--exclude-standard', '-z')):
        changed.update(p for p in git(repo, *args).split('\0') if p)
    if not changed.issubset(targets):
        raise PublicationRefused('Unexpected files changed; preserve for review')
    if not changed:
        return None  # Never push an unrelated existing history for a no-op run.
    git(repo, 'add', '--all', '--', *sorted(changed))
    git(repo, '-c', 'commit.gpgsign=false', 'commit', '--only', '-m',
        'chore: refresh outbound artifacts', '--', *sorted(changed))
    commit = git(repo, 'rev-parse', 'HEAD')
    if git(repo, 'rev-list', '--parents', '-n', '1', commit).split() != [commit, base]:
        raise PublicationRefused('Generated commit has unexpected parents')
    if set(git(repo, 'diff-tree', '--no-commit-id', '--name-only', '-r', '-z', commit).split('\0')) - {''} != changed:
        raise PublicationRefused('Commit includes unexpected paths')
    validate_identity(repo, expected_remote)
    if git(repo, 'status', '--porcelain', '--untracked-files=all') or git(repo, 'rev-parse', 'HEAD') != commit:
        raise PublicationRefused('Checkout changed before publication')
    # Exact SHA and exact expected tip: another publisher advancing main rejects this push.
    git(repo, 'push', '--porcelain', '--no-follow-tags', '--recurse-submodules=no',
        '--force-with-lease=refs/heads/main:' + base,
        expected_remote, commit + ':refs/heads/main')
    return commit

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import safe_publication as publication

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='git-hardening-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'checkout'
        self.remote = self.root / 'remote.git'
        self.repo.mkdir()
        # Isolated config and only filesystem transport allowed for EVERY Git subprocess.
        self.env = patch.dict(os.environ, {'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                                          'GIT_ALLOW_PROTOCOL': 'file', 'GIT_TERMINAL_PROMPT': '0'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.git('init', '--quiet', '--initial-branch=main')
        self.git('config', 'user.name', 'Synthetic')
        self.git('config', 'user.email', 'synthetic@localhost')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', 'NUL')
        (self.repo / 'artifact.txt').write_text('baseline')
        self.git('add', 'artifact.txt')
        self.git('commit', '--quiet', '-m', 'Synthetic baseline')
        self.git('init', '--bare', '--quiet', str(self.remote))
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '--quiet', 'origin', 'main')
        self.base = publication.begin(self.repo, str(self.remote))

    def git(self, *args):
        return subprocess.run(['git', '-c', 'core.hooksPath=NUL', '-C', str(self.repo), *args],
                              check=True, capture_output=True, text=True, timeout=10).stdout.strip()

    def remote_head(self):
        return self.git('--git-dir=' + str(self.remote), 'rev-parse', 'refs/heads/main')

    def change(self):
        (self.repo / 'artifact.txt').write_text('generated')

    def publish(self):
        return publication.publish(self.repo, self.base, ['artifact.txt'], str(self.remote))

    def test_exact_generated_commit_published_to_local_bare_repo(self):
        self.change()
        commit = self.publish()
        self.assertEqual(self.remote_head(), commit)
        self.assertEqual(self.git('rev-list', '--parents', '-n', '1', commit).split(), [commit, self.base])

    def test_no_changes_never_push(self):
        with patch.object(publication, 'git', wraps=publication.git) as commands:
            self.assertIsNone(self.publish())
        self.assertFalse(any(call.args[1] == 'push' for call in commands.call_args_list))

    def test_follow_tags_configuration_does_not_publish_extra_refs(self):
        self.git('config', 'push.followTags', 'true')
        self.git('tag', '-a', 'synthetic-private-tag', '-m', 'Synthetic tag')
        self.change()
        self.publish()
        self.assertEqual(self.git('--git-dir=' + str(self.remote), 'for-each-ref', 'refs/tags'), '')

    def test_existing_local_commit_refused(self):
        self.git('commit', '--allow-empty', '--quiet', '-m', 'Unrelated')
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(self.repo, str(self.remote))
        self.assertEqual(self.remote_head(), self.base)

    def test_wrong_branch_and_detached_head_refused(self):
        self.git('checkout', '--quiet', '-b', 'other')
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(self.repo, str(self.remote))
        self.git('checkout', '--quiet', '--detach')
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(self.repo, str(self.remote))

    def test_wrong_remote_and_pushurl_refused(self):
        self.git('remote', 'set-url', '--push', 'origin', str(self.root / 'unexpected.git'))
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(self.repo, str(self.remote))

    def test_unexpected_generated_file_refused_without_commit(self):
        self.change()
        (self.repo / 'unrelated.txt').write_text('concurrent task')
        with self.assertRaises(publication.PublicationRefused):
            self.publish()
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_head_changed_during_generation_refused(self):
        self.git('commit', '--allow-empty', '--quiet', '-m', 'Concurrent')
        self.change()
        with self.assertRaises(publication.PublicationRefused):
            self.publish()
        self.assertEqual(self.remote_head(), self.base)

    def test_remote_race_rejected_by_exact_lease(self):
        self.change()
        competitor = self.git('commit-tree', self.base + '^{tree}', '-p', self.base, '-m', 'Competitor')
        original = publication.git
        def race(repo, *args, **kwargs):
            if args[0] == 'push':
                self.git('push', '--quiet', str(self.remote), competitor + ':refs/heads/main')
            return original(repo, *args, **kwargs)
        with patch.object(publication, 'git', side_effect=race):
            with self.assertRaises(publication.PublicationRefused):
                self.publish()
        self.assertEqual(self.remote_head(), competitor)
        self.assertNotEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_commit_failure_never_pushes_and_preserves_generated_file(self):
        self.change()
        original = publication.git
        def fail_commit(repo, *args, **kwargs):
            if 'commit' in args:
                raise publication.PublicationRefused('Synthetic persistence failure')
            return original(repo, *args, **kwargs)
        with patch.object(publication, 'git', side_effect=fail_commit) as commands:
            with self.assertRaises(publication.PublicationRefused):
                self.publish()
        self.assertFalse(any(call.args[1] == 'push' for call in commands.call_args_list))
        self.assertEqual(self.remote_head(), self.base)
        self.assertEqual((self.repo / 'artifact.txt').read_text(), 'generated')

    def test_url_rewrite_configuration_requires_review(self):
        self.git('config', 'url.file:///synthetic-unused/.insteadOf', 'https://synthetic.invalid/')
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(self.repo, str(self.remote))



    def test_hostile_git_environment_is_neutralized(self):
        foreign = self.root / 'foreign-index'
        foreign.write_text('do not touch')
        hostile = {'GIT_DIR': str(self.root / 'nonexistent-git'),
                   'GIT_WORK_TREE': str(self.root / 'unrelated-tree'),
                   'GIT_INDEX_FILE': str(foreign), 'GIT_COMMON_DIR': str(self.root),
                   'GIT_OBJECT_DIRECTORY': str(self.root / 'objects'),
                   'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.bare',
                   'GIT_CONFIG_VALUE_0': 'true'}
        with patch.dict(os.environ, hostile):
            self.assertEqual(publication.begin(self.repo, str(self.remote)), self.base)
            self.change()
            commit = self.publish()
        self.assertEqual(self.remote_head(), commit)
        self.assertEqual(foreign.read_text(), 'do not touch')
        self.assertFalse((self.root / 'unrelated-tree').exists())

    def test_subdirectory_cannot_impersonate_registered_root(self):
        nested = self.repo / 'nested'
        nested.mkdir()
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(nested, str(self.remote))

    def test_linked_worktree_with_shared_git_directory_refused(self):
        linked = self.root / 'linked'
        self.git('worktree', 'add', '--detach', str(linked), self.base)
        with self.assertRaises(publication.PublicationRefused):
            publication.begin(linked, str(self.remote))


if __name__ == '__main__':
    unittest.main(verbosity=2)

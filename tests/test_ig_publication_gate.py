from pathlib import Path
import unittest
from unittest import mock
from scripts import ig_auto_post

class PublicationGateTests(unittest.TestCase):
    def test_credentials_never_implicitly_enable_publication(self):
        for configured in (False, True):
            with self.subTest(configured=configured), \
                 mock.patch.object(ig_auto_post, 'TOKEN', 'fake' if configured else ''), \
                 mock.patch.object(ig_auto_post, 'IG', 'fake' if configured else ''), \
                 mock.patch.object(ig_auto_post, 'REPO', 'fake/repo'), \
                 mock.patch.object(ig_auto_post, 'api') as api, \
                 mock.patch.object(ig_auto_post, 'run') as git, \
                 mock.patch.object(ig_auto_post, 'cover') as render, \
                 mock.patch.object(ig_auto_post.os, 'makedirs') as mkdir:
                with self.assertRaisesRegex(ValueError, 'Publication disabled'):
                    ig_auto_post.main([])
                for operation in (api, git, render, mkdir):
                    operation.assert_not_called()

    def test_workflow_is_validation_only(self):
        text = (Path(__file__).resolve().parents[1] / '.github/workflows/ig-auto-post.yml').read_text()
        self.assertIn('contents: read', text)
        self.assertIn('persist-credentials: false', text)
        self.assertNotIn('secrets.', text)
        self.assertNotIn('contents: write', text)
        commands = [line.strip() for line in text.splitlines() if 'python scripts/ig_auto_post.py' in line]
        self.assertEqual(commands, ['run: python scripts/ig_auto_post.py --dry-run'])

if __name__ == '__main__':
    unittest.main()

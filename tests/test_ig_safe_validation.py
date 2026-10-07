import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from scripts.ig_content_validation import normalize_slide, validate_queue
from scripts import ig_auto_post

TOPIC = {"id": "test", "badge": "Teste", "title": "Titulo", "caption": "Legenda",
         "slides": [["Contexto", "Valor", "Descricao", "Nota adicional"]]}

class InstagramValidationTests(unittest.TestCase):
    def test_three_fields(self):
        self.assertEqual(normalize_slide(["a", "b", "c"]), ("a", "b", "c"))

    def test_four_fields_preserves_note(self):
        self.assertEqual(normalize_slide(["a", "b", "c", "d"]), ("a", "b", "c\nd"))

    def test_invalid_lengths(self):
        for slide in ([], ["a", "b"], ["a"] * 5, "abc"):
            with self.subTest(slide=slide), self.assertRaises(ValueError):
                normalize_slide(slide)

    def test_invalid_field_types(self):
        for field in (None, 1, "", " "):
            with self.subTest(field=field), self.assertRaises(ValueError):
                normalize_slide(["a", "b", field])

    def test_input_is_not_mutated(self):
        original = copy.deepcopy(TOPIC)
        validate_queue([TOPIC])
        self.assertEqual(TOPIC, original)

    def test_empty_queue(self):
        with self.assertRaises(ValueError):
            validate_queue([])

    def test_required_fields(self):
        for field in ("id", "badge", "title", "caption"):
            topic = dict(TOPIC); topic.pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_queue([topic])

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            validate_queue([TOPIC, TOPIC])

    def test_carousel_limit(self):
        topic = dict(TOPIC, slides=[["a", "b", "c"]] * 9)
        with self.assertRaises(ValueError):
            validate_queue([topic])

    def test_repository_queue(self):
        queue_path = Path(__file__).resolve().parents[1] / 'scripts/ig_content_queue.json'
        queue = json.loads(queue_path.read_text(encoding='utf-8'))
        valid = validate_queue(queue)
        self.assertEqual(len(valid), len(queue))
        self.assertTrue(all(len(slide) == 3 for topic in valid for slide in topic['slides']))

    def test_dry_run_no_side_effects(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'queue.json'
            path.write_text(json.dumps([TOPIC]), encoding='utf-8')
            with mock.patch.object(ig_auto_post, 'api') as api, \
                 mock.patch.object(ig_auto_post, 'run') as git, \
                 mock.patch.object(ig_auto_post, 'cover') as render, \
                 mock.patch.object(ig_auto_post.os, 'makedirs') as mkdir, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ig_auto_post.main(['--dry-run', '--queue', str(path)]), 0)
                api.assert_not_called(); git.assert_not_called()
                render.assert_not_called(); mkdir.assert_not_called()

    def test_missing_credentials_fail_before_side_effects(self):
        with mock.patch.object(ig_auto_post, 'TOKEN', ''), \
             mock.patch.object(ig_auto_post, 'api') as api, \
             mock.patch.object(ig_auto_post, 'run') as git, \
             mock.patch.object(ig_auto_post, 'cover') as render:
            with self.assertRaises(ValueError):
                ig_auto_post.main([])
            api.assert_not_called(); git.assert_not_called(); render.assert_not_called()

if __name__ == '__main__':
    unittest.main()

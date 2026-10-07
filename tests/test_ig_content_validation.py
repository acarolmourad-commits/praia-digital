import ast
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
source_path = root / 'scripts' / 'ig_auto_post.py'
if not source_path.exists():
    source_path = Path(__file__).with_name('ig_auto_post.py')
tree = ast.parse(source_path.read_text(encoding='utf-8'))
ns = {}
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ('normalize_slide', 'validate_queue')]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source_path), 'exec'), ns)
normalize_slide = ns['normalize_slide']
validate_queue = ns['validate_queue']

def topic():
    return dict(id='example', badge='Example', title='Example title', caption='Example caption', slides=[['a', 'b', 'c']])

class ContentValidationTests(unittest.TestCase):
    def test_three_fields(self):
        self.assertEqual(normalize_slide(['a', 'b', 'c']), ('a', 'b', 'c'))
    def test_four_fields_preserved(self):
        self.assertEqual(normalize_slide(['a', 'b', 'c', 'd']), ('a', 'b', 'c\nd'))
    def test_invalid_slide(self):
        for slide in ([], ['a', 'b'], ['a', 'b', 'c', 'd', 'e'], ['a', 'b', None], ['a', 'b', '']):
            with self.subTest(slide=slide), self.assertRaises(ValueError):
                normalize_slide(slide)
    def test_valid_queue(self):
        value=[topic()]
        self.assertEqual(validate_queue(value), value)
    def test_invalid_queue(self):
        for value in ([], {}, [{'id': 'example'}], [topic(), topic()]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_queue(value)
    def test_too_many_slides(self):
        value=topic(); value['slides']=[['a', 'b', 'c'] for _ in range(9)]
        with self.assertRaises(ValueError):
            validate_queue([value])

if __name__ == '__main__':
    unittest.main()

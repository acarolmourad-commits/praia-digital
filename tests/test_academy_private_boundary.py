import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class PrivateBoundary(unittest.TestCase):
 def test_current_checkout_has_no_new_full_material(self):
  guard=module('boundary','scripts/check_academy_private_boundary.py');self.assertEqual(guard.violations(ROOT),[])
 def test_guard_blocks_reintroduced_source_and_output(self):
  guard=module('boundary','scripts/check_academy_private_boundary.py')
  with tempfile.TemporaryDirectory() as temp:
   r=Path(temp);p=r/'docs/academy/course-learning-plans-new.json';p.parent.mkdir(parents=True);p.write_text('{}');o=r/'docs/academy/delivery/test.html';o.parent.mkdir();o.write_text('fixture')
   self.assertEqual(len(guard.violations(r)),2)
 def test_generator_requires_external_inputs_and_output(self):
  builder=module('builder','scripts/build_academy_digital.py')
  with self.assertRaises(ValueError):builder.build()
  with tempfile.TemporaryDirectory() as temp:
   with self.assertRaisesRegex(ValueError,'outside'):builder.build(Path(temp)/'source.json',ROOT/'docs/academy/delivery')
 def test_private_output_rejects_linked_file(self):
  builder=module('builder','scripts/build_academy_digital.py')
  with tempfile.TemporaryDirectory() as temp:
   directory=Path(temp).resolve();target=directory/'course.html';target.symlink_to(ROOT/'README.md')
   with self.assertRaisesRegex(ValueError,'linked'):builder.private_target(directory,'course')
 def test_legacy_modules_preserved_and_no_automatic_claim(self):
  self.assertEqual(len(list((ROOT/'education/cursos').glob('*/curso-completo/modulo-*.md'))),268)
  metadata=json.loads((ROOT/'docs/academy/public-offer-map.json').read_text());self.assertEqual(len(metadata['course_slugs']),62)
  self.assertNotIn('courses',metadata)
  for f in ['.github/workflows/academy-ci.yml','scripts/prepare_academy_publication.py']:
   self.assertIn('check_academy_private_boundary',(ROOT/f).read_text())

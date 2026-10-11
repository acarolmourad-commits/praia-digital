import importlib.util, json, tempfile, unittest
from pathlib import Path
SPEC = importlib.util.spec_from_file_location("public_builder", Path(__file__).resolve().parents[1]/"scripts/prepare_pages_public.py")
MODULE = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MODULE)
class PublicArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.source = self.root/"checkout"; self.source.mkdir()
        (self.source/"index.html").write_text("<h1>Public fixture</h1>")
        (self.source/"docs/sales").mkdir(parents=True)
        (self.source/"docs/sales/example.csv").write_text("SYNTHETIC ONLY")
        self.output = self.root/"public"
    def manifest(self, files): return {"version":1,"reviewed":True,"files":files}
    def reject(self, value, output=None):
        with self.assertRaises(ValueError): MODULE.prepare(self.source, output or self.output, value)
        self.assertFalse(self.output.exists())
    def test_only_explicit_files(self):
        self.assertEqual(MODULE.prepare(self.source,self.output,self.manifest(["index.html"])),1)
        self.assertEqual([p.name for p in self.output.rglob("*")],["index.html"])
    def test_unreviewed(self): self.reject({"version":1,"reviewed":False,"files":["index.html"]})
    def test_empty(self): self.reject(self.manifest([]))
    def test_internal_even_if_listed(self): self.reject(self.manifest(["docs/sales/example.csv"]))
    def test_traversal(self): self.reject(self.manifest(["../index.html"]))
    def test_absolute(self): self.reject(self.manifest(["/index.html"]))
    def test_backslash(self): self.reject(self.manifest(["docs\\index.html"]))
    def test_hidden(self): self.reject(self.manifest([".env"]))
    def test_symlink(self):
        (self.source/"alias.html").symlink_to(self.source/"index.html")
        self.reject(self.manifest(["alias.html"]))
    def test_symlink_directory(self):
        (self.source/"alias").symlink_to(self.source,target_is_directory=True)
        self.reject(self.manifest(["alias/index.html"]))
    def test_output_symlink_parent(self):
        (self.root/"alias").symlink_to(self.source,target_is_directory=True)
        self.reject(self.manifest(["index.html"]),self.root/"alias/public")
    def test_duplicate(self): self.reject(self.manifest(["index.html","index.html"]))
    def test_missing(self): self.reject(self.manifest(["absent.html"]))
    def test_existing_output(self):
        self.output.mkdir(); (self.output/"keep.txt").write_text("KEEP")
        with self.assertRaises(ValueError): MODULE.prepare(self.source,self.output,self.manifest(["index.html"]))
        self.assertEqual((self.output/"keep.txt").read_text(),"KEEP")
    def test_output_inside_source(self): self.reject(self.manifest(["index.html"]),self.source/"public")
    def test_disallowed_file_type(self):
        (self.source/"example.csv").write_text("SYNTHETIC ONLY")
        self.reject(self.manifest(["example.csv"]))
if __name__ == "__main__": unittest.main()

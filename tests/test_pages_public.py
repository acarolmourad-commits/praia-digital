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
        (self.source/"docs/sales/example.html").write_text("SYNTHETIC ONLY")
        self.output = self.root/"public"
    def manifest(self, files): return {"version":1,"reviewed":True,"files":files}
    def reject(self, value, output=None):
        with self.assertRaises(ValueError): MODULE.prepare(self.source, output or self.output, value)
        self.assertFalse(self.output.exists())
    def reject_internal(self, name):
        fixture = self.source/name
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text("SYNTHETIC ONLY", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "^Blocked internal or hidden path$"):
            MODULE.prepare(self.source, self.output, self.manifest([name]))
        self.assertFalse(self.output.exists())
    def test_only_explicit_files(self):
        self.assertEqual(MODULE.prepare(self.source,self.output,self.manifest(["index.html"])),1)
        self.assertEqual([p.name for p in self.output.rglob("*")],["index.html"])
    def test_unreviewed(self): self.reject({"version":1,"reviewed":False,"files":["index.html"]})
    def test_empty(self): self.reject(self.manifest([]))
    def test_internal_even_if_listed(self): self.reject_internal("docs/sales/example.html")
    def test_blocked_directories_with_allowed_extensions(self):
        # Independent expected policy: do not derive cases from MODULE.BLOCKED.
        directories = ("docs", "leads", "outreach", "csv-lotes-email", "propostas", "backup", "backups", "backend", "automation", "scripts", "tests", "admin", "uploads", "api", "dashboard", "dashboards", "lead", "node_modules")
        for directory in directories:
            for spelling in (directory, directory.upper()):
                for suffix in ("html", "json"):
                    for prefix in ("", "nested/"):
                        name = prefix + spelling + "/fixture." + suffix
                        with self.subTest(name=name): self.reject_internal(name)
    def test_explicit_blocked_paths(self):
        names = ("ferramentas/airbnb-admin.html", "FERRAMENTAS/AIRBNB-ADMIN.HTML", "education/cursos/_archive/index.html", "education/cursos/_archive/fixture.json", "education/marketing/campaigns/index.html", "education/marketing/campaigns/fixture.json", "EDUCATION/CURSOS/_ARCHIVE/fixture.json", "EDUCATION/MARKETING/CAMPAIGNS/index.html")
        for name in names:
            with self.subTest(name=name): self.reject_internal(name)
    def test_blocked_file_path_descendants(self):
        self.reject_internal("ferramentas/airbnb-admin.html/fixture.json")
    def test_allowed_resources_and_prefix_siblings(self):
        fixtures = {"index.html":"<h1>Public fixture</h1>", "assets/site.css":"body { color: black; }", "js/site.js":"console.log('SYNTHETIC ONLY');", "assets/public.json":'{"synthetic": true}', "ferramentas/airbnb-admin-public.html":"<h1>Synthetic public sibling</h1>", "education/cursos/_archive-public/index.html":"<h1>Synthetic public sibling</h1>", "education/marketing/campaigns-public/index.html":"<h1>Synthetic public sibling</h1>"}
        for name, content in fixtures.items():
            fixture = self.source/name
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.write_text(content, encoding="utf-8")
        self.assertEqual(MODULE.prepare(self.source, self.output, self.manifest(list(fixtures))), len(fixtures))
        actual = {p.relative_to(self.output).as_posix() for p in self.output.rglob("*") if p.is_file()}
        self.assertEqual(actual, set(fixtures))
        for name, content in fixtures.items():
            self.assertEqual((self.output/name).read_text(encoding="utf-8"), content)
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

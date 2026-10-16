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
    def test_root_operational_pages_blocked(self):
        names = ("acoes-hoje.html", "acompanhamento-prospeccao.html", "top5-leads-hoje.html")
        for name in names:
            for spelling in (name, name.upper(), name.title()):
                with self.subTest(name=spelling): self.reject_internal(spelling)
    def test_root_operational_path_descendants_blocked(self):
        names = ("acoes-hoje.html", "acompanhamento-prospeccao.html", "top5-leads-hoje.html")
        for name in names:
            for spelling in (name, name.upper()):
                path = spelling + "/fixture.json"
                with self.subTest(name=path): self.reject_internal(path)
    def test_root_operational_prefix_siblings_allowed(self):
        names = ("acoes-hoje-public.html", "acompanhamento-prospeccao-public.html", "top5-leads-hoje-public.html")
        for name in names:
            (self.source/name).write_text("<h1>SYNTHETIC ONLY</h1>", encoding="utf-8")
        self.assertEqual(MODULE.prepare(self.source, self.output, self.manifest(list(names))), len(names))
        actual = {p.relative_to(self.output).as_posix() for p in self.output.rglob("*") if p.is_file()}
        self.assertEqual(actual, set(names))
        for name in names:
            self.assertEqual((self.output/name).read_text(encoding="utf-8"), "<h1>SYNTHETIC ONLY</h1>")
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
    def test_manifest_version_type_strict(self):
        for version in (True, 1.0, "1", None, 0, 2):
            with self.subTest(version=version):
                self.reject({"version": version, "reviewed": True, "files": ["index.html"]})
    def test_manifest_integer_version_one_allowed(self):
        self.assertEqual(MODULE.prepare(self.source, self.output, self.manifest(["index.html"])), 1)
    def test_casefold_duplicate_paths(self):
        self.reject(self.manifest(["index.html", "INDEX.HTML"]))
    def test_file_directory_conflict_both_orders(self):
        for names in (["fixture.html", "fixture.html/child.html"], ["FIXTURE.HTML/child.html", "fixture.html"]):
            with self.subTest(names=names):
                with self.assertRaisesRegex(ValueError, "File and directory path conflict"):
                    MODULE.prepare(self.source, self.output, self.manifest(names))
                self.assertFalse(self.output.exists())
    def test_control_and_incompatible_paths(self):
        names = ("nul\x00.html", "tab\t.html", "newline\n.html", "del\x7f.html", "control\x85.html", "C:/index.html", "C:index.html", "asset:stream.html", "star*.html", "query?.html", "quote\".html", "less<.html", "greater>.html", "pipe|.html", "folder./index.html", "folder /index.html", "folder/CON.html", "aux.html", "LPT1.html", "COM9.html")
        for name in names:
            with self.subTest(name=repr(name)):
                with self.assertRaisesRegex(ValueError, "Invalid relative path"):
                    MODULE.prepare(self.source, self.output, self.manifest([name]))
                self.assertFalse(self.output.exists())
    def test_safe_prefix_siblings_allowed(self):
        names = ["folder/index.html", "folder-more/index.html", "COM10.html"]
        for name in names:
            fixture=self.source/name; fixture.parent.mkdir(parents=True, exist_ok=True); fixture.write_text("SYNTHETIC ONLY")
        self.assertEqual(MODULE.prepare(self.source,self.output,self.manifest(names)),3)
    def test_source_root_symlink(self):
        alias=self.root/"source-alias"; alias.symlink_to(self.source,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Symlinks are not allowed"):
            MODULE.prepare(alias,self.output,self.manifest(["index.html"]))
        self.assertFalse(self.output.exists())
    def test_source_parent_symlink(self):
        alias=self.root/"parent-alias"; alias.symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Symlinks are not allowed"):
            MODULE.prepare(alias/"checkout",self.output,self.manifest(["index.html"]))
        self.assertFalse(self.output.exists())
    def test_source_dangling_symlink(self):
        alias=self.root/"dangling-source"; alias.symlink_to(self.root/"missing")
        with self.assertRaisesRegex(ValueError,"Symlinks are not allowed"):
            MODULE.prepare(alias,self.output,self.manifest(["index.html"]))
        self.assertFalse(self.output.exists())
    def test_output_symlink_external_parent(self):
        external=self.root/"external"; external.mkdir(); alias=self.root/"output-alias"; alias.symlink_to(external,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Symlinks are not allowed"):
            MODULE.prepare(self.source,alias/"public",self.manifest(["index.html"]))
        self.assertEqual(list(external.iterdir()),[])
    def test_output_dangling_symlink(self):
        target=self.root/"missing-output"; self.output.symlink_to(target)
        with self.assertRaisesRegex(ValueError,"Symlinks are not allowed"):
            MODULE.prepare(self.source,self.output,self.manifest(["index.html"]))
        self.assertFalse(target.exists()); self.assertTrue(self.output.is_symlink())
    def test_output_dangling_symlink_parent(self):
        target=self.root/"missing-parent"; alias=self.root/"dangling-parent"; alias.symlink_to(target,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Symlinks are not allowed"):
            MODULE.prepare(self.source,alias/"public",self.manifest(["index.html"]))
        self.assertFalse(target.exists()); self.assertTrue(alias.is_symlink())
if __name__ == "__main__": unittest.main()

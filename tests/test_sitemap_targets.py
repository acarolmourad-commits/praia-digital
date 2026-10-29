"""Regression coverage for the offline sitemap gate."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from xml.sax.saxutils import escape

SPEC = importlib.util.spec_from_file_location(
    "sitemap_targets", Path(__file__).resolve().parents[1] / "scripts/validate_sitemap_targets.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class SitemapTargetsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sitemap = self.root / "sitemap.xml"

    def write_sitemap(self, urls):
        self.sitemap.write_text(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + ''.join(f'<url><loc>{escape(url)}</loc></url>' for url in urls)
            + '</urlset>', encoding="utf-8"
        )

    def validate(self, urls):
        self.write_sitemap(urls)
        return validator.validate_sitemap(self.sitemap, self.root)

    def test_existing_file_directory_home_and_encoded_unicode(self):
        (self.root / "index.html").touch()
        (self.root / "apps").mkdir()
        (self.root / "apps/index.html").touch()
        (self.root / "avaliação.html").touch()
        self.assertEqual([], self.validate([
            "https://praia.digital/", "https://praia.digital/index.html",
            "https://praia.digital/apps/", "https://praia.digital/apps",
            "https://praia.digital/avalia%C3%A7%C3%A3o.html",
        ]))

    def test_omits_explicit_noindex_and_meta_refresh_pages(self):
        page = self.root / "page.html"
        for markup in ['<meta name="robots" content="noindex, follow">',
                       "<META CONTENT='NONE' NAME='ROBOTS'>",
                       '<meta name="googlebot" content="max-snippet:20 noindex">',
                       '<meta http-equiv="REFRESH" content="0; url=/destination.html">']:
            with self.subTest(markup=markup):
                page.write_text(markup)
                errors = self.validate(["https://praia.digital/page.html"])
                self.assertEqual(len(errors), 1)
                self.assertIn("non-indexable target", errors[0])

    def test_indexable_pages_are_not_removed_for_unrelated_text(self):
        page = self.root / "page.html"
        for markup in ['<meta name="robots" content="index, follow">',
                       '<meta name="robots" content="nofollow">',
                       '<meta name="description" content="noindex">',
                       '<p>Explain noindex and redirects.</p>',
                       '<!-- <meta name="robots" content="noindex"> -->',
                       '<script>const example = \'<meta name="robots" content="noindex">\';</script>']:
            with self.subTest(markup=markup):
                page.write_text(markup)
                self.assertEqual(self.validate(["https://praia.digital/page.html"]), [])

    def test_directory_index_obeys_robots_directive(self):
        (self.root / "apps").mkdir()
        (self.root / "apps/index.html").write_text('<meta name="robots" content="noindex">')
        self.assertIn("non-indexable target", self.validate(["https://praia.digital/apps/"])[0])

    def test_missing_file_and_directory_without_index(self):
        (self.root / "empty").mkdir()
        errors = self.validate([
            "https://praia.digital/docs/sales/deleted.html", "https://praia.digital/empty/"
        ])
        self.assertEqual(2, len(errors))
        self.assertTrue(all("missing local target" in error for error in errors))

    def test_duplicate_url(self):
        (self.root / "index.html").touch()
        self.assertIn("duplicate URL", self.validate(["https://praia.digital/"] * 2)[0])

    def test_external_origin_query_fragment_and_unsafe_paths(self):
        for url in ["https://example.com/", "http://praia.digital/",
                    "https://praia.digital/?page=1", "https://praia.digital/#home",
                    "https://praia.digital/%2e%2e/index.html", "https://praia.digital/%00.html"]:
            with self.subTest(url=url):
                self.assertTrue(self.validate([url]))

    def test_symlink_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "external.html"
            target.touch()
            (self.root / "escape.html").symlink_to(target)
            self.assertIn("escapes site root", self.validate(["https://praia.digital/escape.html"])[0])

    def test_directory_index_symlink_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "external.html"
            target.touch()
            (self.root / "apps").mkdir()
            (self.root / "apps/index.html").symlink_to(target)
            self.assertIn("escapes site root", self.validate(["https://praia.digital/apps/"])[0])

    def test_missing_or_malformed_sitemap(self):
        self.assertTrue(validator.validate_sitemap(self.sitemap, self.root))
        self.sitemap.write_text("<broken>")
        self.assertIn("cannot read sitemap", validator.validate_sitemap(self.sitemap, self.root)[0])

    def test_empty_sitemap_and_missing_loc(self):
        self.assertIn("no URLs", self.validate([])[0])
        self.sitemap.write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url/></urlset>')
        self.assertIn("missing loc", validator.validate_sitemap(self.sitemap, self.root)[0])

    def test_rejects_wrong_document_type(self):
        self.sitemap.write_text('<html/>')
        self.assertIn("expected sitemap urlset", validator.validate_sitemap(self.sitemap, self.root)[0])


if __name__ == "__main__":
    unittest.main()

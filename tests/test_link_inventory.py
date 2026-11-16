import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from link_inventory import inspect_links

class LinkInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'páginas').mkdir()
        (self.root / 'páginas/index.html').touch()
        (self.root / 'empty').mkdir()
        (self.root / 'asset.css').touch()

    def scan(self, text, page='index.html'):
        return inspect_links(text, page, self.root)

    def test_actual_attributes_and_percent_encoding(self):
        bad, external = self.scan('<A HREF = /p%C3%A1ginas/?q=1&amp;x=2#top>ok</A><img src="/asset.css"><!-- <a href="/missing"> -->')
        self.assertEqual((bad, external), ([], []))

    def test_absolute_same_host_and_protocol_relative(self):
        bad, external = self.scan('<a href="https://praia.digital/missing"></a><a href="//www.praia.digital/páginas/"></a>')
        self.assertEqual(len(bad), 1)
        self.assertEqual(external, [])

    def test_script_templates_are_not_html_links(self):
        self.assertEqual(self.scan('<script>const s = `<a href="/missing">`;</script><a href="${url}">x</a>'), ([], []))

    def test_root_relative_parent_segments_and_base(self):
        self.assertEqual(self.scan('<a href="../asset.css"></a>'), ([], []))
        self.assertEqual(self.scan('<base href="/páginas/"><a href="../asset.css"></a>'), ([], []))

    def test_empty_directory_does_not_count_as_page(self):
        self.assertEqual(len(self.scan('<a href="/empty/"></a>')[0]), 1)

    def test_external_inventory_is_not_a_success_claim(self):
        bad, external = self.scan('<a href="https://example.org/?a=1&amp;b=2#top">x</a><a href="mailto:foo@example.org">mail</a>')
        self.assertEqual(bad, [])
        self.assertEqual(external, ['https://example.org/?a=1&b=2'])

if __name__ == '__main__':
    unittest.main()

"""Keep the published HTML safe before the local-only module initializes."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class OficinaSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / 'apps/oficina-ia-imobiliaria/index.html').read_text()
        cls.tags = Markup(cls.html).tags

    def test_forms_cannot_fall_back_to_get_or_post(self):
        forms = [attrs for tag, attrs in self.tags if tag == 'form']
        self.assertEqual({form['id'] for form in forms}, {'listing', 'followup'})
        for form in forms:
            self.assertEqual(form.get('method'), 'dialog')
        for _, attrs in self.tags:
            self.assertNotIn('formaction', attrs)
            self.assertNotIn('formmethod', attrs)

    def test_every_tool_control_starts_disabled(self):
        controls = [(tag, attrs) for tag, attrs in self.tags
                    if tag in ('input', 'textarea', 'select', 'button')]
        self.assertGreaterEqual(len(controls), 20)
        for tag, attrs in controls:
            with self.subTest(tag=tag, control=attrs.get('name', attrs.get('id'))):
                self.assertIn('disabled', attrs)
                self.assertIn('data-oficina-control', attrs)

    def test_failure_message_and_editorial_fallback_remain_available(self):
        notice = [attrs for _, attrs in self.tags if attrs.get('id') == 'startup-status']
        self.assertEqual(len(notice), 1)
        self.assertNotIn('hidden', notice[0])
        self.assertEqual(notice[0]['role'], 'status')
        self.assertIn('<noscript>', self.html)
        self.assertIn('href="/blog/briefing-imobiliario-para-ia.html"', self.html)


if __name__ == '__main__':
    unittest.main()

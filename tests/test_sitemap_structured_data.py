"""Every inline JSON-LD block on a submitted page must parse as JSON."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class StructuredDataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            media_type = (dict(attrs).get('type') or '').partition(';')[0]
            if media_type.strip().lower() == 'application/ld+json':
                self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.blocks.append(''.join(self.current))
            self.current = None


class PublishedStructuredDataTests(unittest.TestCase):
    def test_jsonld_in_sitemap_pages(self):
        urls = set()
        for sitemap in [*ROOT.glob('sitemap*.xml'), ROOT / 'raw.xml']:
            urls.update(loc.text for loc in ET.parse(sitemap).findall('.//{*}loc'))
        for url in sorted(urls):
            path = ROOT / unquote(urlsplit(url).path).lstrip('/')
            if path.is_dir():
                path /= 'index.html'
            parser = StructuredDataParser()
            parser.feed(path.read_text(encoding='utf-8'))
            parser.close()
            with self.subTest(url=url):
                self.assertIsNone(parser.current, 'unclosed JSON-LD script')
                for block in parser.blocks:
                    json.loads(block)

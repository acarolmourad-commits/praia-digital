from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_contact_email import transform


class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.hrefs = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.hrefs.append(dict(attrs).get('href'))


class EmailContactTest(unittest.TestCase):
    def check_output(self, source):
        page = Path('imoveis/exemplo.html')
        out = transform(source, page)
        self.assertEqual(transform(out, page), out)
        return out

    def test_recipient_body_and_accessible_name(self):
        src = '<title>Casa &amp; praia</title><a aria-label="WhatsApp" href="https://wa.me/11954346288?text=Visita%20A%26B%20%231" target="_blank">Pedir pelo WhatsApp</a>'
        out = self.check_output(src)
        dest = urlsplit(Links(out).hrefs[0])
        self.assertEqual((dest.scheme, dest.path), ('mailto', 'comercial@praia.digital'))
        self.assertEqual(parse_qs(dest.query), {'subject':['Contato — Casa & praia'], 'body':['Visita A&B #1']})
        self.assertIn('Pedir por e-mail', out)
        self.assertNotIn('target="_blank"', out)

    def test_legacy_utm_quote(self):
        src = '<a href="https://wa.me/5511954346288?utm_source=site"text=Quero%20uma%20visita" rel="noopener">Contato</a>'
        href = Links(self.check_output(src)).hrefs[0]
        self.assertEqual(parse_qs(urlsplit(href).query)['body'], ['Quero uma visita'])

    def test_share_and_other_recipients(self):
        src = '<a href="https://wa.me/?text=link">Compartilhar</a><a href="https://wa.me/5513999999999">Parceiro</a>'
        self.assertEqual(self.check_output(src), src)

    def test_form_and_composed_javascript(self):
        src = '<form action="https://wa.me/5511954346288" method="get"></form><script>location.href="https://wa.me/5511954346288?text="+encodeURIComponent(text)</script>'
        out = self.check_output(src)
        self.assertIn('data-pd-email-form',out)
        self.assertIn('/js/contact-email-form.js',out)
        self.assertIn('&body="+encodeURIComponent(text)',unescape(out))

    def test_json_ld_keeps_other_identities(self):
        src = '<script type="application/ld+json">{"sameAs":["https://wa.me/5511954346288","https://example.org/id"]}</script>'
        self.assertIn('"sameAs": ["https://example.org/id"]', self.check_output(src))

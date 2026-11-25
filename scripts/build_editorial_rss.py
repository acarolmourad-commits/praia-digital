"""Build the public RSS feed from articles featured on the blog landing page."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

from validate_sitemap_targets import NAMESPACE, canonical_sitemap_path, indexing_exclusions

ROOT = Path(__file__).resolve().parents[1]
BLOG = 'https://praia.digital/blog/index.html'
ATOM = 'http://www.w3.org/2005/Atom'


class ArticleLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'a' and values.get('href'):
            self.links.append(urljoin(BLOG, values['href']).split('#')[0])
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def build(root=ROOT):
    root = Path(root)
    approved = {node.text for node in ET.parse(root / 'sitemap.xml').iter(f'{{{NAMESPACE}}}loc')}
    landing = ArticleLinks()
    landing.feed((root / 'blog/index.html').read_text(encoding='utf-8'))
    ET.register_namespace('atom', ATOM)
    feed = ET.Element('rss', version='2.0')
    channel = ET.SubElement(feed, 'channel')
    ET.SubElement(channel, 'title').text = 'Blog Praia Digital'
    ET.SubElement(channel, 'link').text = BLOG
    ET.SubElement(channel, 'description').text = 'Guias e artigos em destaque sobre imóveis e hospedagem no litoral.'
    ET.SubElement(channel, 'language').text = 'pt-BR'
    ET.SubElement(channel, f'{{{ATOM}}}link', href='https://praia.digital/rss.xml', rel='self', type='application/rss+xml')
    for url in dict.fromkeys(landing.links):
        if url not in approved or url == BLOG:
            continue
        rel = urlsplit(url).path.lstrip('/')
        if not rel.startswith('blog/') or not rel.endswith('.html'):
            continue
        page = root / rel
        if canonical_sitemap_path(page, root) != rel or indexing_exclusions(page):
            continue
        article = ArticleLinks()
        article.feed(page.read_text(encoding='utf-8'))
        title = ' '.join(''.join(article.title).split())
        if not title:
            continue
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = url
        ET.SubElement(item, 'guid', isPermaLink='true').text = url
        if len(channel.findall('item')) == 25:
            break
    if not channel.findall('item'):
        raise ValueError('The blog landing page contains no eligible articles')
    ET.indent(feed, space='  ')
    return ET.tostring(feed, encoding='utf-8', xml_declaration=True) + b'\n'


if __name__ == '__main__':
    (ROOT / 'rss.xml').write_bytes(build())


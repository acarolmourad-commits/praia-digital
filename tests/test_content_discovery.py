import importlib.util
import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('discovery', ROOT/'scripts/build-content-discovery.py')
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.ids=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a' and 'href' in attrs: self.links.append(attrs['href'])
        if 'id' in attrs: self.ids.append(attrs['id'])

class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries,cls.skipped=discovery.collect(ROOT)
        cls.pages=[ROOT/'sitemap.html',*sorted((ROOT/'explorar').glob('pagina-*.html'))]

    def test_catalog_matches_eligible_sitemaps(self):
        self.assertEqual(json.loads((ROOT/'data/content-search.json').read_text()),self.entries)
        self.assertTrue(all(discovery.visitor_excluded(unquote(urlsplit(url).path).lstrip('/')) for url in self.skipped))
        self.assertGreater(len(self.entries),5000)
        self.assertEqual(len({e['url'] for e in self.entries}),len(self.entries))

    def test_internal_operations_not_promoted_as_visitor_content(self):
        for path in ['docs/sales/index.html','docs/materiais/pagina-execucao.html','central-comando-praia-digital.html','dashboard-prospeccao.html']:
            self.assertTrue(discovery.visitor_excluded(path))
        for path in ['docs/inteligencia/boletim-diario.html','docs/guia-copy-anuncios-imoveis-litoral-2026.html','blog/index.html']:
            self.assertFalse(discovery.visitor_excluded(path))

    def test_all_entries_have_crawlable_links_without_javascript(self):
        links=set()
        for page in self.pages: links.update(Links(page.read_text()).links)
        self.assertTrue({e['url'] for e in self.entries} <= links)
        for page in self.pages: self.assertIn('/'+page.relative_to(ROOT).as_posix(),links)

    def test_generated_pages_are_current(self):
        count=(len(self.entries)+discovery.PAGE_SIZE-1)//discovery.PAGE_SIZE
        self.assertEqual(len(self.pages),count)
        for number in range(1,count+1):
            path=ROOT/discovery.page_url(number).lstrip('/')
            self.assertEqual(path.read_text(),discovery.render(self.entries,number,count))

    def test_new_links_and_fragments_resolve(self):
        guides=[ROOT/url.lstrip('/') for url,_,_ in discovery.FEATURED[:3]]
        for page in [*self.pages,*guides]:
            parsed=Links(page.read_text())
            self.assertEqual(len(parsed.ids),len(set(parsed.ids)),page)
            for link in parsed.links:
                parts=urlsplit(link)
                if parts.netloc: continue
                target=ROOT/unquote(parts.path).lstrip('/') if parts.path else page
                if target.is_dir(): target/= 'index.html'
                self.assertTrue(target.is_file(),(page,link))
                if parts.fragment: self.assertIn(parts.fragment,Links(target.read_text()).ids)

    def test_index_excludes_aliases_noindex_redirects_and_blocked_pages(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            pages={'good.html':'','hidden.html':'<meta name="robots" content="noindex">',
                   'redirect.html':'<meta http-equiv="refresh" content="0;url=/good.html">',
                   'blocked.html':'','alias.html':''}
            (root/'robots.txt').write_text('User-agent: *\nDisallow: /blocked.html\n')
            for name,meta in pages.items():
                canonical='good.html' if name=='alias.html' else name
                (root/name).write_text(f'<html><head><title>A &amp; B</title>{meta}<link rel="canonical" href="https://praia.digital/{canonical}"></head><body>Public</body></html>')
            (root/'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://praia.digital/{name}</loc></url>' for name in pages)+'</urlset>')
            entries,skipped=discovery.collect(root)
            self.assertEqual([e['url'] for e in entries],['/good.html'])
            self.assertEqual(entries[0]['title'],'A & B')
            self.assertEqual(len(skipped),4)

    def test_new_guides_are_reachable_from_related_hubs(self):
        sources={'ficha-comparacao-bairros-litoral':['index.html','cidades/index.html','bairros/index.html'],
                 'auditoria-fotos-descricao-temporada':['blog/index.html','meu-imovel.html','servicos/anuncios-airbnb-booking.html'],
                 'conferencia-calendarios-temporada':['blog/index.html','meu-imovel.html','ferramentas/index.html']}
        for slug,pages in sources.items():
            for page in pages: self.assertIn('/guias/'+slug+'.html',Links((ROOT/page).read_text()).links)
        self.assertIn('class="pd-site-search" href="/sitemap.html"',(ROOT/'partials/header.html').read_text())

if __name__=='__main__': unittest.main()

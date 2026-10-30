import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
PAGES=['servicos/anuncios-airbnb-booking.html','servicos/edicao-anuncios-airbnb-booking.html','anfitrioes/central-priceplabs.html']
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
class ServicePromotionSafety(unittest.TestCase):
    def test_no_unverified_payment_or_performance_claims(self):
        forbidden=['buy.stripe.com','+64%','zero horas','Sem overbooking','lota sua agenda','máquina de reservas','aparece mais alto','cartão, Pix ou boleto','até 5 dias úteis','SEU_AFFILIATE','YOUR_AFFILIATE','O pagamento é processado pela Stripe','procedimentos informados no checkout']
        for path in PAGES:
            source=(ROOT/path).read_text()
            for text in forbidden:self.assertNotIn(text,source,path)
    def test_blocked_service_checkout_routes_to_consultation(self):
        services=(ROOT/'servicos.html').read_text()
        diagnostics=(ROOT/'anfitrioes/diagnosticos-anfitrioes.html').read_text()
        self.assertNotIn('7sY9AU3tC21h4Tl5pu4ZR1X',services)
        self.assertNotIn('bJeeVeaW4fS7gC3bNS4ZR24',diagnostics)
        self.assertIn('R$ 499 por plataforma',services)
        self.assertIn('consulta_diagnostico_precificacao',diagnostics)
        self.assertIn('Pagamento a confirmar com a equipe',diagnostics)
        self.assertNotIn('Você será direcionado ao checkout externo',diagnostics)
        self.assertIn('Confirme como pagar',diagnostics)
        # Unrelated services are not silently reassigned to these products.
        self.assertIn('bJe28sd4c0XdfxZ19e4ZR1Y',services)
        self.assertIn('14A7sMc08bBR99BaJO4ZR25',diagnostics)
        self.assertIn('00w8wQ7JS35l99B19e4ZR23',diagnostics)
    def test_listing_prices_and_exclusions_remain(self):
        for path in PAGES[:2]:
            source=(ROOT/path).read_text()
            for text in ['499','998','por plataforma','Não incluído','PriceLabs','sob consulta','senhas','antes','pagamento']:
                self.assertIn(text,source,path)
        source=(ROOT/PAGES[2]).read_text()
        self.assertIn('Gestão de preços com PriceLabs',source)
        self.assertIn('R$ 499,00',source)
        self.assertIn('Não. A ferramenta',source)
    def test_schema_is_valid_and_truthful(self):
        for path in PAGES:
            source=(ROOT/path).read_text()
            for script in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',source,re.S):
                json.loads(script)
        source=(ROOT/PAGES[0]).read_text()
        self.assertNotIn('schema.org/InStock',source)
        self.assertIn('"price":"499.00"',source)
    def test_academy_link_preview_only(self):
        source=(ROOT/PAGES[1]).read_text()
        self.assertIn('/education/cursos/airbnb-do-zero/amostra.html',source)
        self.assertIn('não inclui compra, acesso integral ou acompanhamento humano',source)
        self.assertNotIn('/academy/cursos/',source)
        self.assertNotIn('precificação dinâmica',source)
    def test_contrast_overrides_survive_shared_styles(self):
        self.assertIn('section.cta{background:linear-gradient', (ROOT/PAGES[0]).read_text())
        self.assertIn('.hero .btn-secondary{background:#15385b', (ROOT/PAGES[2]).read_text())
    def test_local_links_resolve(self):
        for page in PAGES:
            p=Parser();p.feed((ROOT/page).read_text())
            for href in p.links:
                u=urlsplit(href)
                if u.scheme or u.netloc:continue
                if u.path:
                    target=ROOT/u.path.lstrip('/') if u.path.startswith('/') else (ROOT/page).parent/u.path
                    if target.is_dir():target=target/'index.html'
                    self.assertTrue(target.is_file(),f'{page}: {href}')
                else:target=ROOT/page
                if u.fragment:
                    other=Parser();other.feed(target.read_text())
                    self.assertIn(unquote(u.fragment),other.ids,f'{page}: {href}')

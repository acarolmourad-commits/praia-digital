"""Keep the actual calendar walkthrough one click from the two host decisions."""
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "/guias/conferencia-calendarios-temporada.html#conferencia"
STAYS = "anfitrioes/central-stays.html"


class HostCalendarDiscoveryTests(unittest.TestCase):
    def test_booking_channel_manager_card_keeps_both_routes(self):
        html = (ROOT / "anfitrioes/central-booking.html").read_text(encoding="utf-8")
        integrations = html.split('<section id="integracoes"', 1)[1].split("</section>", 1)[0]
        card = integrations.split("<h3>Gestor de canais</h3>", 1)[1].split("</article>", 1)[0]
        self.assertIn(f'href="{GUIDE}">Conferir calendários de temporada', card)
        self.assertIn('href="central-stays.html"', card)
        self.assertIn("nem conecta automaticamente contas", integrations)

    def test_listing_service_points_to_walkthrough_without_promising_access(self):
        html = (ROOT / "servicos/anuncios-airbnb-booking.html").read_text(encoding="utf-8")
        card = html.split("Orientação entre plataformas</h3>", 1)[1].split("</div>", 1)[0]
        self.assertIn("Quando aplicável ao escopo, orientamos a conferência", card)
        self.assertIn("O roteiro não conecta contas nem altera reservas.", card)
        self.assertEqual(re.findall(r'href="([^"]+)"', card), [GUIDE, "/" + STAYS])
        self.assertIn('href="/guias/conferencia-calendarios-temporada.html"', html)

    def test_guide_and_stays_are_valid_targets(self):
        guide = urlsplit(GUIDE)
        html = (ROOT / guide.path.lstrip("/")).read_text(encoding="utf-8")
        self.assertIn(f'id="{guide.fragment}"', html)
        self.assertIn(f'rel="canonical" href="https://praia.digital{guide.path}"', html)
        self.assertIn("sem alterá-las", html)
        self.assertTrue((ROOT / STAYS).is_file())

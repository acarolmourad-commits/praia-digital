import json
import tempfile
import unittest
from pathlib import Path

from scripts.public_inventory_scope import catalog_paths, excluded_from_public_index


class PublicInventoryScopeTests(unittest.TestCase):
    def test_exact_catalog_paths_preserve_confirmed_property_and_root_alias(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'js').mkdir()
            (root / 'js/main.js').write_text('const properties = ' + json.dumps([
                {'slug': 'casa-confirmada'}, {'slug': '../casa-catalogo'}
            ]) + ';')
            self.assertEqual(catalog_paths(root), {'imoveis/casa-confirmada.html', 'casa-catalogo.html'})
            self.assertFalse(excluded_from_public_index('imoveis/casa-confirmada.html', root))
            self.assertTrue(excluded_from_public_index('imoveis/casa-nao-confirmada-bertioga.html', root))
            self.assertFalse(excluded_from_public_index('blog/guia-santos.html', root))
            self.assertFalse(excluded_from_public_index('cidades/santos.html', root))

    def test_private_sections_do_not_hide_public_newsletters_or_backup_guide(self):
        for path in ['newsletter/drafts/edicao.html', 'exclusivos/conteudo.html']:
            self.assertTrue(excluded_from_public_index(path))
        for path in ['newsletter/edicao.html', 'blog/backup-seguranca-dados.html']:
            self.assertFalse(excluded_from_public_index(path))

    def test_search_index_does_not_offer_properties_outside_active_catalog(self):
        root = Path(__file__).resolve().parents[1]
        entries = json.loads((root / 'data/content-search.json').read_text())
        for entry in entries:
            self.assertFalse(excluded_from_public_index(entry['url'], root), entry['url'])


if __name__ == '__main__':
    unittest.main()

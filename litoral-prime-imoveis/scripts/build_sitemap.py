"""Build the secondary sitemap using the shared reviewed indexing rules."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from gerar_sitemaps import discover_pages, write

def main():
    pages, _ = discover_pages(ROOT)
    urls = [url for url in pages if url.startswith('litoral-prime-imoveis/')]
    write(ROOT / 'litoral-prime-imoveis/sitemap.xml', urls)
    print('secondary sitemap:', len(urls), 'URLs')

if __name__ == '__main__':
    main()

"""Render the same complete app directory on every app. No data or calculations change."""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render(groups, current=None):
    esc = html.escape
    sections = []
    for group in groups:
        links = []
        for app in group['apps']:
            if app['slug'] == current:
                continue
            links.append(f'<li><a href="/apps/{esc(app["slug"])}/"><strong>{esc(app["title"])}</strong><span>{esc(app["description"])}</span></a></li>')
        if links:
            sections.append(f'<div class="pd-network-group"><h3>{esc(group["title"])}</h3><ul class="pd-network-grid">{"".join(links)}</ul></div>')
    return ('<section class="pd-network" aria-labelledby="pd-network-title">'
            '<h2 id="pd-network-title">Continue com o próximo aplicativo</h2>'
            '<p class="pd-network-intro">Use uma ficha conferida, anote suas premissas e escolha o recurso da próxima etapa. Você pode voltar ao catálogo a qualquer momento.</p>'
            '<details><summary>Explorar a rede completa de aplicativos</summary>' + ''.join(sections) + '</details>'
            '<p><a href="/apps/">Catálogo de aplicativos</a> · <a href="/#rede-apps">Roteiros na página inicial</a> · <a href="/servicos.html">Apoio profissional</a></p>'
            '<p class="pd-network-note">Os links não transferem dados automaticamente. Confira fontes, datas, custos e limitações antes de decidir. Simulações não são laudos, aprovação de crédito nem garantia de retorno.</p></section>')

def build(root=ROOT, check=False):
    groups = json.loads((root / 'data/app-network.json').read_text(encoding='utf-8'))
    slugs = [a['slug'] for g in groups for a in g['apps']]
    actual = {p.parent.name for p in (root / 'apps').glob('*/index.html')}
    if len(slugs) != len(set(slugs)) or set(slugs) != actual:
        raise ValueError('App registry must match every published app exactly once')
    changed = []
    for slug in [None] + slugs:
        path = root / 'apps' / (slug or '') / 'index.html'
        text = path.read_text(encoding='utf-8')
        network = render(groups, slug)
        pattern = r'<section\b[^>]*class="pd-network"[^>]*>[\s\S]*?</section>'
        if re.search(pattern, text):
            updated = re.sub(pattern, lambda _: network, text, count=1)
        else:
            updated = text.replace('</body>', '\n' + network + '\n</body>')
        if '/css/app-network.css' not in updated:
            updated = updated.replace('</head>', '<link rel="stylesheet" href="/css/app-network.css">\n</head>')
        if updated != text:
            changed.append(str(path.relative_to(root)))
            if not check:
                path.write_text(updated, encoding='utf-8')
    return changed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = build(check=args.check)
    print(json.dumps({'changed': changed}, ensure_ascii=False))
    raise SystemExit(1 if args.check and changed else 0)

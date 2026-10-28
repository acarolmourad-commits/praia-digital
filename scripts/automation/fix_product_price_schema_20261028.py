#!/usr/bin/env python3
"""
fix_product_price_schema_20261028.py

Corrige o erro critico do Search Console "Snippets do produto":
"O formato do preco na propriedade price e invalido (em offers)".

Transformacoes (idempotentes):
1) Em imoveis/*.html (inclui template-landing.html):
   - offers.price como objeto AggregateOffer -> offers vira AggregateOffer
     no nivel certo (priceCurrency, lowPrice, highPrice, availability,
     seller preservados). Nenhum preco novo e inventado.
   - Bloco RealEstateListing duplicado com "price": "Sob consulta":
     remove price/priceCurrency nao-numericos desse bloco.
2) Geradores (para nao recriar o erro):
   - scripts/batch_seo_changes.py: remove price/priceCurrency textuais
     do build_jsonld.
   - scripts/automation/add_listing_schema.py: so inclui price quando
     numerico; fallback textual removido.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
IMOVEIS = ROOT / "imoveis"
LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

stats = {"files_changed": 0, "aggregate_fixed": 0, "sob_consulta_removed": 0, "blocks_unparsed": 0}


def transform(obj):
    changed = False
    if not isinstance(obj, dict):
        return obj, changed
    offers = obj.get("offers")
    if isinstance(offers, dict):
        price = offers.get("price")
        if isinstance(price, dict) and price.get("@type") == "AggregateOffer":
            new_offers = {
                "@type": "AggregateOffer",
                "priceCurrency": offers.get("priceCurrency", "BRL"),
                "lowPrice": price.get("lowPrice"),
                "highPrice": price.get("highPrice"),
            }
            if "offerCount" in price:
                new_offers["offerCount"] = price["offerCount"]
            if "availability" in offers:
                new_offers["availability"] = offers["availability"]
            if "seller" in offers:
                new_offers["seller"] = offers["seller"]
            for k, v in offers.items():
                if k not in new_offers and k != "price":
                    new_offers[k] = v
            obj["offers"] = new_offers
            stats["aggregate_fixed"] += 1
            changed = True
    if obj.get("price") == "Sob consulta":
        del obj["price"]
        obj.pop("priceCurrency", None)
        stats["sob_consulta_removed"] += 1
        changed = True
    return obj, changed


def fix_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    file_changed = False

    def repl(m):
        nonlocal file_changed
        head, body, tail = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(body.strip())
        except Exception:
            stats["blocks_unparsed"] += 1
            return m.group(0)
        items = data if isinstance(data, list) else [data]
        block_changed = False
        new_items = []
        for item in items:
            item, ch = transform(item)
            block_changed = block_changed or ch
            new_items.append(item)
        if not block_changed:
            return m.group(0)
        file_changed = True
        new_data = new_items if isinstance(data, list) else new_items[0]
        return head + "\n" + json.dumps(new_data, ensure_ascii=False, indent=2) + "\n" + tail

    new_text = LD_RE.sub(repl, text)
    if file_changed and new_text != text:
        path.write_text(new_text, encoding="utf-8")
        stats["files_changed"] += 1
        return True
    return False


def fix_generators():
    fixed = []
    batch = ROOT / "scripts" / "batch_seo_changes.py"
    if batch.exists():
        t = batch.read_text(encoding="utf-8", errors="ignore")
        old = '        "price": "Sob consulta",\n        "priceCurrency": "BRL",\n'
        if old in t:
            batch.write_text(t.replace(old, "", 1), encoding="utf-8")
            fixed.append("scripts/batch_seo_changes.py")
    listing = ROOT / "scripts" / "automation" / "add_listing_schema.py"
    if listing.exists():
        t = listing.read_text(encoding="utf-8", errors="ignore")
        orig = t
        t = t.replace("    return 'Consulte'\n", "    return ''\n", 1)
        old_offers = (
            "        'offers': {\n"
            "            '@type': 'Offer',\n"
            "            'price': price,\n"
            "            'priceCurrency': 'BRL',\n"
            "            'availability': 'https://schema.org/InStock',\n"
            "        },"
        )
        new_offers = (
            "        'offers': {\n"
            "            '@type': 'Offer',\n"
            "            **({'price': price, 'priceCurrency': 'BRL'} if str(price).isdigit() else {}),\n"
            "            'availability': 'https://schema.org/InStock',\n"
            "        },"
        )
        if old_offers in t:
            t = t.replace(old_offers, new_offers, 1)
        if t != orig:
            listing.write_text(t, encoding="utf-8")
            fixed.append("scripts/automation/add_listing_schema.py")
    return fixed


def main():
    for path in sorted(IMOVEIS.glob("*.html")):
        fix_html(path)
    fixed_generators = fix_generators()
    print("files_changed=", stats["files_changed"])
    print("aggregate_fixed=", stats["aggregate_fixed"])
    print("sob_consulta_removed=", stats["sob_consulta_removed"])
    print("blocks_unparsed=", stats["blocks_unparsed"])
    print("generators_fixed=", ",".join(fixed_generators))


if __name__ == "__main__":
    main()

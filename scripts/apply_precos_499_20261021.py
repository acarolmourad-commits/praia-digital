#!/usr/bin/env python3
"""One-shot (2026-10-21): R$ 500 -> R$ 499 for the two ad-creation services.

Stripe (created 2026-10-21, on the EXISTING products, no duplicates):
- Anuncios Airbnb/Booking prod_VTivRQPU62qSFD:
  price_1USxLzJRA2AketBhf8AmiNdq (49900 BRL), link
  plink_1USxMBJRA2AketBhzRXqodgx https://buy.stripe.com/7sY9AU3tC21h4Tl5pu4ZR1X
- Propaganda imobiliaria prod_VTjFfiQeSyVcWn:
  price_1USxLzJRA2AketBhTGyHF2M9 (49900 BRL), link
  plink_1USxMBJRA2AketBhIwn3KeJm https://buy.stripe.com/bJe28sd4c0XdfxZ19e4ZR1Y
Old R$ 500 links stay active until the site is live, then are deactivated.

Site changes (4 HTML files): every 'R$ 500' for these services becomes
'R$ 499', derived 'R$ 1.000' (2 x 500) becomes 'R$ 998' (2 x 499),
JSON-LD price '500' becomes '499', and old Stripe URLs become the new ones.
All other '500' occurrences in these files are CSS (font-weight/z-index)
and are not touched (only 'R$ 500' / 'R$ 1.000' / URLs are replaced).
Fails closed if counts differ. Idempotent.
"""
from pathlib import Path

OLD_SEASONAL = "https://buy.stripe.com/fZu00k6FO49padFg484ZR1V"
NEW_SEASONAL = "https://buy.stripe.com/7sY9AU3tC21h4Tl5pu4ZR1X"
OLD_PROP = "https://buy.stripe.com/dRm9AUc08eO3adFf044ZR1W"
NEW_PROP = "https://buy.stripe.com/bJe28sd4c0XdfxZ19e4ZR1Y"

# path: (old_seasonal_count, old_prop_count, r500_count, r1000_count)
EXPECTED = {
    "index.html": (0, 0, 3, 0),
    "servicos.html": (1, 1, 6, 1),
    "servicos/propaganda-imobiliaria.html": (0, 2, 5, 0),
    "servicos/anuncios-airbnb-booking.html": (1, 0, 7, 3),
}


def edit(path, counts):
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    if "R$ 499" in text and OLD_SEASONAL not in text and OLD_PROP not in text:
        print(f"already applied {path}")
        return
    exp_seasonal, exp_prop, exp_500, exp_1000 = counts
    found = (text.count(OLD_SEASONAL), text.count(OLD_PROP), text.count("R$ 500"), text.count("R$ 1.000"))
    if found != counts:
        raise SystemExit(f"{path}: expected counts {counts}, found {found}")
    text = text.replace(OLD_SEASONAL, NEW_SEASONAL)
    text = text.replace(OLD_PROP, NEW_PROP)
    text = text.replace("R$ 1.000", "R$ 998")
    text = text.replace("R$ 500", "R$ 499")
    if path.endswith("propaganda-imobiliaria.html"):
        if text.count('"price": "500"') != 1:
            raise SystemExit("propaganda JSON-LD price 500 not found exactly once")
        text = text.replace('"price": "500"', '"price": "499"')
    if "R$ 500" in text or "R$ 1.000" in text or OLD_SEASONAL in text or OLD_PROP in text:
        raise SystemExit(f"{path}: residual old price/link after replacement")
    target.write_text(text, encoding="utf-8")
    print(f"updated {path}")


def main():
    for path, counts in EXPECTED.items():
        edit(path, counts)
    print("OK: R$ 499 applied; 2 units = R$ 998")


if __name__ == "__main__":
    main()

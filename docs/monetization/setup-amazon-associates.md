# Amazon Associates Setup — Praia Digital

**Program:** Amazon Associates  
**Target Storefront:** Brazil / International  
**Status:** READY FOR ACCOUNT CREATION
**StoreID:** `praiadigital-20`

---

## Why Amazon Associates for Praia Digital

Praia Digital visitors are actively researching:
- Home office equipment for remote work
- Smart home devices for seasonal rentals
- Furniture/decor for investment properties
- Real estate investment books
- Photography/video equipment for listings

These convert to Amazon product purchases with 1-3% commissions.

---

## After Approval: Product Linking

### High-Intent Product Categories

| Category | Example ASIN Search | Commission |
|----------|---------------------|------------|
| Home office | standing desk, monitor arm | 1-3% |
| Smart home | smart lock, video doorbell | 1-3% |
| Books | real estate investing | 4-5% |
| Camera gear | mirrorless camera, tripod | 1-3% |
| Furniture | outdoor furniture, storage | 1-3% |

### How to Create Links

1. In Associates Central → Product Linking → Create a link
2. Search products on amazon.com.br or amazon.com
3. Choose format:
   - **Text + Image** for in-content
   - **Banner** for sidebar/footer
   - **Native Shopping Ads** for ad units

### Disclosure Requirement

Add to all pages with affiliate links:
```
Esta página pode conter links de afiliados. Isso significa que posso receber uma comissão se você fizer uma compra através dos links, sem nenhum custo adicional para você.
```

### Link Format

Always append `?tag=praiadigital-20` to Amazon product links, or use the standard Associates link builder with StoreID `praiadigital-20`.

Example:
- Product URL: `https://www.amazon.com.br/dp/B0XXXXXX`
- Affiliate URL: `https://www.amazon.com.br/dp/B0XXXXXX?tag=praiadigital-20`

CTA format: **Conferir na Amazon ➔**
Avoid: "Preço Atualizado"

---

## Integration Checklist

- [ ] Associates account approved
- [ ] Store ID/tracking ID obtained
- [ ] First 5 product links created
- [ ] Disclosure added to pages
- [ ] Links tested: click → product page with ?tag=YOUR_TAG
- [ ] Earnings dashboard bookmarked

---

## Notes

- Do NOT share tracking ID publicly in code repos; inject from environment at build time
- Avoid "Preço Atualizado" CTAs per existing policy
- CTA format per memory: "Conferir na Amazon ➔"

---

*Guide generated: 2026-09-05*

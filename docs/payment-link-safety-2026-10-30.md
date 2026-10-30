# Payment-link safety — 2026-10-30

## Verified service checkout update — 16:05 UTC

The authorized active Stripe account was verified enabled for charges and payouts with no outstanding requirements. Three active LIVE Payment Links were created and independently read back, with exact one-time BRL prices and quantity 1: listing for one property/platform R$499; both platforms for the same property R$998; one-off pricing diagnostic R$499. Public allowlist: `assets/data/service-payment-links.json`.

The site presents these links only after scope-confirmation guidance. Payment does not imply instant service delivery or Academy access. Continuous PriceLabs management remains separately quoted. No checkout transaction was performed, and unrelated payment links are unchanged. Legacy Academy sales remain paused and their public-source protection limitation remains unresolved.

## Earlier state at 12:50 UTC

No new Stripe checkout is published. The confirmed active merchant account is not currently enabled for charges; the authenticated Stripe integration rejected Payment Link creation. Three service product/price definitions were prepared separately, but there are no verified new payment URLs. Account remediation belongs to the owner in Stripe; no credentials, revenue declarations or payment-method settings are changed here.

- Listing service remains R$499 for one property/listing/platform; both platforms for the same property remain R$998.
- The old listing checkout in `servicos.html` now leads to the detailed assisted offer.
- The old pricing-diagnostic checkout in `anfitrioes/diagnosticos-anfitrioes.html` now leads to scoped consultation. R$499 is a one-off diagnostic, not ongoing PriceLabs management.
- Legacy Academy purchase destinations under `academy/cursos/*/index.html` are disabled pending protected delivery. Existing content, student links and course prices are not reassigned to human-service products.
- Other services and their distinct checkout destinations are not silently replaced merely because their prices match. They require separate merchant/product verification before promotion.

## Content-protection limitation

Removing a purchase CTA does not protect content. Full Academy sources and earlier student materials remain accessible in the public repository; excluding generated workbooks from GitHub Pages is not authorization. No repository visibility, history rewrite or student entitlement changes are included.

Recommended zero-new-monthly-cost route: private Workspace storage with named-buyer access; verify the actual paid transaction and exact product before assisted Gmail delivery, and record transaction/delivery status. No immediate or autonomous fulfillment promise until a working integration is deployed and verified. A Drive folder with domain-wide readers is not suitable for buyer-only access.

References checked 2026-10-30:
- https://support.google.com/drive/answer/7166529
- https://support.google.com/drive/answer/2494893
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

Historical copies/forks cannot be revoked by deleting a file from the current branch. Restricting future copies requires a separate owner-approved migration, not a misleading "protected" label.

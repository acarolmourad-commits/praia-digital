# Service promotion safety — 30 October 2026

Scope: listing creation/editing landing pages and the linked PriceLabs central. No Academy/student materials, credentials, infrastructure, Stripe configuration or campaign messages changed.

- Preserve R$499 per listing/platform and R$998 for the same property on both platforms.
- Preserve quoted PriceLabs management separately from the R$499 one-off diagnostic.
- Replace unsupported percentage/client-case, no-work, calendar-conflict, ranking and occupancy promises with clear deliverables and limits.
- Confirm scope, required material, timing, revisions, publication responsibility and payment method before charging; do not assert payment methods or a universal five-day SLA without verification.
- No photography, ongoing guest/price management, software subscriptions or Academy content automatically included.
- The old Academy cross-link now points only to a free sample and explicitly does not grant full access or human accompaniment.

## Existing payment links

Read-only authenticated listing of Payment Links for the owner-confirmed live Stripe account returned an empty list (no further page). This does not prove the previously embedded links are invalid, but their merchant/product/price/method configuration could not be verified against that account. Reversible site CTAs therefore request scope/payment confirmation through the existing business contact instead of sending visitors directly to those links. No Stripe object was modified, deactivated or created.

## Fresh verification

Uncached HTTP reads confirmed the listing-page claims before editing. The current PriceLabs central did not contain affiliate-code placeholders; its Booking search already had no affiliate identifier, so no replacement affiliate code was invented. Existing official resource links and disclosures remain.

Local automated checks cover schema JSON, internal links/anchors, service price distinctions, removed unsupported claims, absence of unverified checkout links and free-preview-only navigation. CI adds390px/1280px browser checks and screenshots, without contact sends, authentication or payments. Publication is not complete until exact commit CI, Pages deployment and live changed-file checks pass.

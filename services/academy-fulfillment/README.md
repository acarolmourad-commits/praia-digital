# Academy fulfillment runtime — disabled draft

No website behavior or live delivery is changed by this directory. There is no deployment workflow. `WEBHOOK_INTAKE_ENABLED`, `AUTOMATIC_DELIVERY_ENABLED` and `WATCHDOG_ENABLED` default to false.

## Architecture
Stripe signs exact webhook bytes → Worker verifies signature, timestamp, merchant/mode and event scope → SQLite Durable Object records events and orders → alarms process bounded work → authenticated Composio **consumer session proxy** revalidates Stripe payment and retrieves owner-only Drive bytes → Gmail draft is verified and sent to the verified buyer.

The public repository contains generic code and synthetic tests only. Private catalog, connection IDs, package files, buyer data and all credentials belong outside Git. Historical public course copies are not protected by this runtime.

## Consumer session, not the legacy proxy
`app/consumer-composio.mjs` is the coordinator default. It calls `/api/v3.1/tool_router/session/{id}/proxy_execute` with `toolkit_slug`, native endpoint, method, parameters and body. It does **not** put developer connection IDs into legacy proxy requests. `drive` maps to `googledrive`.

Consumer requests use `x-user-api-key`, `x-org-id` and `x-project-id`. The user key can reach other projects/apps accessible to its owner; scope headers select a context, not a narrower credential. Keep this broader authorization explicit. Never put the key in chat, tool logs, command-line literals, screenshots, Git or exported session config.

Provision and independently read back a session with exactly three verified account pins, no app-tool allowance, `instant:false`, connection management/workbench/search/multi-execute disabled and session proxy enabled. Tool restrictions do **not** constrain proxy endpoints: the local fixed route allowlist remains mandatory. No public generic proxy endpoint exists. Session config is checked before provider writes; missing/changed allowlists or account pins fail closed. Authentication/approval errors are never bypassed; expired sessions are not recreated automatically.

Configuration (private values, no examples of real IDs):
- `COMPOSIO_USER_API_KEY`, `COMPOSIO_ORG_ID`, `COMPOSIO_CONSUMER_PROJECT_ID`, `COMPOSIO_USER_ID`, `COMPOSIO_CONSUMER_SESSION_ID`.
- `COMPOSIO_CONSUMER_ACCOUNTS_JSON`: exact account pins keyed `stripe`, `gmail`, `googledrive`, verified in that consumer scope.
- `STRIPE_ACCOUNT_ID`, `STRIPE_MODE`, `STRIPE_WEBHOOK_SECRET`, `SENDER_EMAIL`, `TEST_BUYER_EMAIL`.
- `CATALOG_FILE_ID`, `CATALOG_SHA256`, `CATALOG_BYTES`, `EXPECTED_OFFER_COUNT`, `COMPOSIO_DOWNLOAD_HOSTS_JSON`.

Store the owner-only private catalog as `application/octet-stream` with exact original UTF-8 JSON bytes. Catalog maps approved PaymentLink IDs to immutable product/price/edition/package metadata. Never hash reserialized JSON. Actual Composio binary response and download hostname must be verified, not guessed or wildcarded.

## Safety and limitations
- Fresh payment/session/line-item/charge checks; exact price/product/quantity and BRL integration amount. Foreign presentment cannot override base-price validation.
- Unpaid, failed, refunded, disputed or wrong-account payments do not deliver.
- Private Drive ownership/permissions before and after exact byte/hash download.
- Durable order deduplication, leases and compare-and-set state. Stable Message-ID and exact Sent reconciliation. Ambiguous sends are held, never blindly repeated; no exactly-once claim.
- Two events, two pending sessions and one order per alarm; bounded Sent search. Empty queues make no provider calls.
- Input/output storage gates protect storage-only scheduling; provider I/O is outside storage critical sections.
- Custom `wake()` only schedules persisted work. Before production explicitly configure an hourly watchdog cron (for example `17 * * * *`) and enable its flag after approval. This recovers lost alarm retries after quota reset; it does not guarantee immediate delivery.
- Already-delivered attachments cannot be recalled after a later refund. Gmail acceptance is not proof the buyer read the email.

## Verification
Run Node24 `npm ci`, `npm test` (100 offline tests), `npm run build` (Wrangler dry-run only). Tests include SQLite persistence, paid/async/refund cases, private-byte validation, raw MIME tampering, ambiguous send, consumer scope/config drift and synthetic end-to-end coordinator flow.

PR CI also runs real local workerd signed-intake/duplicate/tampered-body checks with delivery disabled and synthetic credentials. The original runtime check passed after pinning the compatibility date to the installed binary; exact revised-head CI must also pass. This is not a real payment/email/provider test.

## Release gates — still blocked until verified
Actual Free-plan entitlement/CPU/memory/quota behavior; safely stored approved credentials; intended identities for every consumer connection; successful authenticated exact-byte catalog/Drive and Gmail MIME TEST; test-mode signed payment to intended test mailbox; duplicates, delayed payments, failures, refund and ambiguous-send checks; hourly watchdog and sanitized operational alerts. No LIVE enablement until those gates and required approval are complete. Do not retry blocked Google OAuth by changing account scopes without authorization.

Official references:
- https://docs.composio.dev/docs/consumer-agents
- https://docs.composio.dev/reference/authenticating-to-composio
- https://docs.composio.dev/reference/api-reference/tool-router/postToolRouterSession
- https://docs.composio.dev/reference/api-reference/tool-router/postToolRouterSessionBySessionIdProxyExecute
- https://docs.composio.dev/docs/extending-sessions/proxy-execute
- https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/
- https://developers.cloudflare.com/durable-objects/api/alarms/
- https://developers.google.com/workspace/gmail/api/guides/sending

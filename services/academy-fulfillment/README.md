# Academy fulfillment runtime — disabled draft

No website behavior or live delivery is changed by this directory. There is no deployment workflow. `WEBHOOK_INTAKE_ENABLED`, `AUTOMATIC_DELIVERY_ENABLED` and `WATCHDOG_ENABLED` default to false.

## Architecture
Stripe signs exact webhook bytes → Worker verifies signature, timestamp, merchant/mode and event scope → SQLite Durable Object records events and orders → alarms process bounded work → an approved direct Stripe restricted read-only key revalidates payment; the authenticated Composio **Google-only consumer session proxy** retrieves owner-only Drive bytes → Gmail draft is verified and sent to the verified buyer.

The public repository contains generic code and synthetic tests only. Private catalog, connection IDs, package files, buyer data and all credentials belong outside Git. Historical public course copies are not protected by this runtime.

## Consumer session, not the legacy proxy
`app/providers.mjs` is the coordinator default: direct restricted Stripe reads plus Google-only `app/consumer-composio.mjs`. It calls `/api/v3.1/tool_router/session/{id}/proxy_execute` with `toolkit_slug`, native endpoint, method, parameters and body. It does **not** put developer connection IDs into legacy proxy requests. `drive` maps to `googledrive`.

Consumer requests use `x-user-api-key`, `x-org-id` and `x-project-id`. Verified API versions can return `ok_`/`pr_` scope nano IDs as well as documented `org_`/`proj_` examples. Consumer connection IDs can also be `ca_`; provenance within the resolved consumer user/project and authoritative identity checks matter, not the prefix alone. The user key can reach other projects/apps accessible to its owner; scope headers select a context, not a narrower credential. Keep this broader authorization explicit. Never put the key in chat, tool logs, command-line literals, screenshots, Git or exported session config.

Provision and independently read back a session with exactly two verified Google account pins, no app-tool allowance, `instant:false`, connection management/workbench/search/multi-execute disabled and session proxy enabled. Tool restrictions do **not** constrain proxy endpoints: the local fixed route allowlist remains mandatory. No public generic proxy endpoint exists. Session config is checked before provider writes; missing/changed allowlists or account pins fail closed. Authentication/approval errors are never bypassed; expired sessions are not recreated automatically.

Configuration (private values, no examples of real IDs):
- `COMPOSIO_USER_API_KEY`, `COMPOSIO_ORG_ID`, `COMPOSIO_CONSUMER_PROJECT_ID`, `COMPOSIO_USER_ID`, `COMPOSIO_CONSUMER_SESSION_ID`.
- `COMPOSIO_CONSUMER_ACCOUNTS_JSON`: exact account pins keyed `gmail`, `googledrive` (no Stripe consumer pin), verified in that consumer scope.
- `STRIPE_ACCOUNT_ID`, `STRIPE_MODE`, `STRIPE_READONLY_API_KEY`, `STRIPE_WEBHOOK_SECRET`, `SENDER_EMAIL`, `TEST_BUYER_EMAIL`.
- `CATALOG_FILE_ID`, `CATALOG_SHA256`, `CATALOG_BYTES`, `EXPECTED_OFFER_COUNT`, `COMPOSIO_DOWNLOAD_HOSTS_JSON`.

Store the owner-only private catalog as `application/octet-stream` with exact original UTF-8 JSON bytes. Catalog maps approved PaymentLink IDs to immutable product/price/edition/package metadata. Never hash reserialized JSON. Actual Composio binary response and download hostname must be verified, not guessed or wildcarded.

## Direct Stripe restricted key
`app/stripe-readonly.mjs` only issues GET requests to the fixed account/session/line-item/payment-intent/charge/dispute routes at api.stripe.com. It accepts a matching test/live restricted-key prefix, not a full secret key. The prefix does NOT prove permissions: setup must verify the actual RAK grants are read-only and scoped to the intended merchant. No Stripe-Account override, refunds, payments, settings or webhook writes are available from runtime. Existing unrelated Composio Stripe connections remain untouched and cannot be selected by the Google-only session. Wrong merchant identity remains a hard failure; never change the expected merchant merely to match a different connection.

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
Run Node24 `npm ci`, `npm test` (110 existing regression cases plus 74 local consolidation cases), `npm run build` (Wrangler dry-run only). Tests include SQLite persistence, paid/async/refund cases, private-byte validation, raw MIME tampering, ambiguous send, consumer scope/config drift and synthetic end-to-end coordinator flow.

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

Stripe restricted-key reference: https://docs.stripe.com/keys

## Local consolidation candidate (not published or activated)

This candidate starts from PR #86 head `5247def7ed7a3546c5314ce029bda53c11473488` and keeps its Durable Object architecture. The separate Node/D1 simulation is a source of contract tests, not another active backend.

- Signed exact-byte SHA-256 and event creation time are now part of immutable receipt identity. A signed receipt conflict is committed as a durable account-shard intake hold before the error reply. All new effects stop until explicit reconciliation. No automatic unhold is provided.
- Order fingerprint conflicts hold the affected order and invalidate in-flight pre-effect CAS. Known or uncertain external effects are preserved; a message already accepted cannot be recalled. A conflict during draft creation keeps the order UNCERTAIN, and a separate hold_reason preserves the incident across recovery. The account-shard receipt hold also pauses automatic reconciliation of effects already in flight; those require manual review.
- Charge status, currency, amount and captured amount must be fully consistent with the successful PaymentIntent. Missing or contradictory fields fail closed.
- Existing databases without receipt payload hashes are refused with `LEDGER_SCHEMA_REVIEW_REQUIRED`. There is no implicit backfill or authorized production migration. Use a fresh local test database.
- The added flow suite uses the real Worker/coordinator/ledger/MIME code under a Node class shim and SQLite/provider fixtures. It is not a workerd or real-provider E2E. All signing values are public fixtures and all recipients are `.invalid`.

Still unresolved before real delivery: complete refund/dispute/charge-history verification, trusted buyer/recipient identity beyond a Checkout email field, authenticated current private catalog/package checks, actual provider TEST, protected credentials, storage migration/reconciliation and verified cost limits. Strict Charge equality only accepts consistent integration-currency data; it is not a new claim of tested cross-currency provider support. All deployed/configured state remains unchanged.


### Final write boundary

A reservation is not final permission to write. Every draft/send now receives a one-use, synchronous ledger guard. After MIME construction and consumer-session preflight, immediately before the outbound provider-write request, the real adapter checks the current hold, state, version, lease owner and unexpired lease. Missing, asynchronous or non-true authorization is rejected. There is no await between this check and issuing the fetch request. This closes the reproduced window where a signed conflict arrived during the preflight GET but the later POST still proceeded.

Tests cover the real ConsumerComposio and AcademyProviders transport paths using fake network responses, including conflicts, revocation, lease expiry, clock reversal, version drift, asynchronous MIME construction and guard reuse. The guard cannot recall a write already issued and does not make Stripe, Drive and Gmail atomic. Real workerd behavior and provider E2E remain release gates.

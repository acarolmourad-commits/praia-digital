# Automatic Academy delivery — local preparation checkpoint
2026-10-31. No external resources/credentials have been created. No mail sent.

## Concrete implementation
Worker entrypoint app/worker.mjs verifies raw Stripe signatures and durably records supported events in SQLite DO. app/coordinator.mjs processes bounded isolated events, delayed payments and outbox states with rearmed alarms. app/composio.mjs uses official v3.1 Proxy Execute wire schema with pinned connected accounts and fixed internal route allowlists; it validates owner-only Drive permissions before/after binary download and exact size/hash. app/payment.mjs performs authoritative payment/account/SKU/price checks. app/gmail.mjs builds and validates owned MIME, exact recipient/attachment, searches actual Sent messages and does not blindly resend ambiguous sends. durable/ is the transactional ledger/state machine.

WEBHOOK_INTAKE_ENABLED=false and AUTOMATIC_DELIVERY_ENABLED=false by default. They MUST remain false until explicit grants, private configuration and successful live-provider TEST proof. No end-to-end production readiness claimed.

## Executed evidence
- 81 passing local tests:12 SQLite +8 proxy/signature +22 payment +25 Gmail +4 Drive +10 integrated coordinator.
- Wrangler4.156.0 deploy --dry-run bundle succeeds; no deployment occurred.
- Real workerd synthetic intake test passed in GitHub Actions (run41222736088): durable signed event intake, duplicate intake, tampered signature rejection and delivery-disabled state. Local development-container execution was blocked; CI used the supported Ubuntu runner. This does not exercise real Composio/Gmail or paid delivery.
- Node mocks are not evidence of Cloudflare CPU compliance or provider OAuth/MIME interoperability.

## Required actual configuration and approval
1. Confirm FREE account plan and hard-limit behavior, one Worker/SQLite namespace, no paid addons or plan upgrade.
2. Register exact TEST then LIVE Stripe webhook events; place whsec only in Cloudflare secret binding.
3. Dedicated Composio project containing only required Stripe, Drive and Gmail connections. A scoped project key granting Proxy execute Write-only; it still permits arbitrary API actions under those connections if stolen, so narrow upstream RAK/OAuth and project isolation are required. No auth-config/connection/webhook-management grant needed at runtime.
4. Stripe readonly session/lineitem/PI/charge/dispute/account; Drive readonly file metadata/permissions/download; Gmail compose/send and read-Sent. New OAuth consent or RAK creation needs exact approval.
5. Pin connection IDs, Composio user identity, merchant/mode, sender, TEST buyer allowlist. Keep all private IDs and approved70offer map outside Git.
6. Owner-only private catalog JSON, pinned bytes/SHA, and an explicit approved presigned-download hostname allowlist observed from authenticated Composio response. Do not wildcard arbitrary download origins.
7. TEST from actual signed Stripe event to commercial mailbox with exact ZIP, duplicates, async/failure, permission/hash drift, refunds and ambiguous-send recovery. Only then enable LIVE after approval.

## Secret transfer: supported route and limit
Cloudflare's authenticated API supports PUT /accounts/{account_id}/workers/scripts/{script_name}/secrets with name/type=secret_text/text; text is writeOnly and sensitive. That does NOT make a literal secret in a tool-call argument/history safe. Preferred: owner enters newly created key in Cloudflare's protected dashboard field, or an explicitly approved authenticated local process pipes it to `wrangler secret put`/bulk via stdin without echo, command-line literal, file in Git, log, screenshot or chat. Do not extract credentials from interactive connector/session storage. No existing secret has been read or transferred here. No new Cloudflare deployment token is needed if the approved connector performs deployment; if GitHub deploy is later desired, its additional token grant is separate.

## Remaining engineering/release limits
Production CPU/memory and provider testing still pending; real Composio binary host/shape and Gmail normalization must be verified with authorized TEST accounts. Alarm rearming covers provider outages but free-quota exhaustion can still delay work; no instant SLA. Durable backups/retention/monitoring need operational validation. Existing event handlers cannot recall attachments already sent after later refund. Default logging is disabled to avoid raw PII exposure; add sanitized metrics/owner alerts before launch without dumping provider responses.

Official schema sources:
https://docs.composio.dev/reference/api-reference/tools/postToolsExecuteProxy
https://docs.composio.dev/reference/authenticating-to-composio/project-api-key-permissions
https://developers.cloudflare.com/workers/configuration/secrets/
https://developers.cloudflare.com/durable-objects/api/alarms/
https://developers.google.com/workspace/gmail/api/guides/sending

## Quota and recovery gates
No provider calls occur when idle or before work is due. Each alarm handles at most2 events,2 pending sessions,1 order; exact Sent search is capped at2 results with incomplete searches held. The watchdog scheduled handler only calls custom wake() RPC to schedule persisted due work; it never directly processes orders. Production configuration must explicitly enable an hourly cron (e.g. 17 * * * *) and WATCHDOG_ENABLED after approval, so exhausted alarm retries can recover after daily quota reset. Defaults have no cron and watchdog is disabled. Verify real Free-plan quotas and monitoring; no guaranteed immediate delivery.

Store the private catalog as an owner-only application/octet-stream Drive file with exact original UTF-8 JSON bytes. The download adapter requires Composio binary_data and verifies those exact bytes; it must never hash reserialized provider JSON. Actual provider binary behavior is a TEST release gate.

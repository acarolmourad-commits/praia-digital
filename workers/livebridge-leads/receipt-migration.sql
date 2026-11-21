-- Additive migration. No backfill, sends, or changes to existing notification rows.
CREATE TABLE IF NOT EXISTS receipt_delivery (
  lead_id TEXT PRIMARY KEY REFERENCES leads(id) ON DELETE CASCADE,
  recipient TEXT NOT NULL,
  message_json TEXT NOT NULL,
  admitted_at TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued',
  started_at TEXT,
  accepted_at TEXT,
  provider_id TEXT,
  error_code TEXT
);
CREATE INDEX IF NOT EXISTS receipt_delivery_admitted ON receipt_delivery(admitted_at);
CREATE INDEX IF NOT EXISTS receipt_delivery_recipient ON receipt_delivery(recipient,admitted_at);

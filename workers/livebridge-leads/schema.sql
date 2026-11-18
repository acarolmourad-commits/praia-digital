CREATE TABLE IF NOT EXISTS leads (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL DEFAULT '',
  business TEXT NOT NULL,
  live_source TEXT NOT NULL,
  marketplaces TEXT NOT NULL,
  destinations TEXT NOT NULL,
  goal TEXT NOT NULL DEFAULT '',
  page_url TEXT NOT NULL,
  utm TEXT NOT NULL,
  consent_version TEXT NOT NULL,
  consent_at TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'novo'
);
CREATE INDEX IF NOT EXISTS leads_created_at ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS leads_email ON leads(email);

CREATE TABLE IF NOT EXISTS service_requests (lead_id TEXT PRIMARY KEY REFERENCES leads(id), service TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS notification_outbox (
lead_id TEXT NOT NULL REFERENCES leads(id), kind TEXT NOT NULL CHECK(kind IN ('team','receipt')),
status TEXT NOT NULL DEFAULT 'pending_setup', created_at TEXT NOT NULL,
sent_at TEXT, provider_id TEXT, PRIMARY KEY(lead_id,kind));
CREATE TRIGGER IF NOT EXISTS lead_notifications AFTER INSERT ON leads BEGIN
INSERT OR IGNORE INTO notification_outbox(lead_id,kind,created_at) VALUES(NEW.id,'team',NEW.created_at);
INSERT OR IGNORE INTO notification_outbox(lead_id,kind,created_at) VALUES(NEW.id,'receipt',NEW.created_at);
END;
INSERT OR IGNORE INTO notification_outbox(lead_id,kind,created_at) SELECT id,'team',created_at FROM leads;
INSERT OR IGNORE INTO notification_outbox(lead_id,kind,created_at) SELECT id,'receipt',created_at FROM leads;

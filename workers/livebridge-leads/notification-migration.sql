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

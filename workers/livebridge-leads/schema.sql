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

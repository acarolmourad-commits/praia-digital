CREATE TABLE IF NOT EXISTS crm_customers (
 id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL, business TEXT NOT NULL DEFAULT '', phone TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS crm_deals (
 id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES crm_customers(id),
 lead_id TEXT UNIQUE REFERENCES leads(id), service TEXT NOT NULL,
 stage TEXT NOT NULL DEFAULT 'novo' CHECK(stage IN ('novo','contato','proposta','negociacao','ganho','perdido')),
 amount_cents INTEGER NOT NULL DEFAULT 0 CHECK(amount_cents>=0),
 received_cents INTEGER NOT NULL DEFAULT 0 CHECK(received_cents>=0 AND received_cents<=amount_cents),
 delivery TEXT NOT NULL DEFAULT 'planejado' CHECK(delivery IN ('planejado','andamento','entregue')),
 due_date TEXT NOT NULL DEFAULT '', next_contact TEXT NOT NULL DEFAULT '',
 next_action TEXT NOT NULL DEFAULT '', owner TEXT NOT NULL DEFAULT 'Comercial',
 description TEXT NOT NULL DEFAULT '', source TEXT NOT NULL DEFAULT 'Formulário',
 archived INTEGER NOT NULL DEFAULT 0 CHECK(archived IN (0,1)),
 version INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 closed_at TEXT, CHECK(received_cents=0 OR stage='ganho')
);
CREATE INDEX IF NOT EXISTS crm_deals_customer ON crm_deals(customer_id);
CREATE TABLE IF NOT EXISTS crm_activity (
 id INTEGER PRIMARY KEY AUTOINCREMENT, deal_id TEXT NOT NULL REFERENCES crm_deals(id),
 created_at TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS crm_activity_deal ON crm_activity(deal_id,id DESC);
CREATE TABLE IF NOT EXISTS crm_auth (
 id TEXT PRIMARY KEY, token_hash TEXT, expires_at INTEGER NOT NULL DEFAULT 0,
 next_send INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS crm_sessions (token_hash TEXT PRIMARY KEY, expires_at INTEGER NOT NULL);
CREATE TRIGGER IF NOT EXISTS crm_deal_created AFTER INSERT ON crm_deals BEGIN
 INSERT INTO crm_activity(deal_id,created_at,kind,body) VALUES(NEW.id,NEW.created_at,'registro','Solicitação registrada: '||NEW.service);
END;
CREATE TRIGGER IF NOT EXISTS crm_deal_updated AFTER UPDATE ON crm_deals BEGIN
 INSERT INTO crm_activity(deal_id,created_at,kind,body) VALUES(NEW.id,NEW.updated_at,'alteracao',json_object('etapa_anterior',OLD.stage,'etapa',NEW.stage,'valor_anterior_centavos',OLD.amount_cents,'valor_centavos',NEW.amount_cents,'recebido_anterior_centavos',OLD.received_cents,'recebido_centavos',NEW.received_cents,'entrega',NEW.delivery,'prazo',NEW.due_date,'retorno',NEW.next_contact,'acao',NEW.next_action,'responsavel',NEW.owner,'arquivado',NEW.archived));
END;
CREATE TRIGGER IF NOT EXISTS crm_capture AFTER INSERT ON service_requests
WHEN EXISTS(SELECT 1 FROM leads WHERE id=NEW.lead_id AND status!='teste_tecnico') BEGIN
 INSERT INTO crm_customers(id,email,name,business,phone,created_at,updated_at)
 SELECT 'lead-'||id,lower(trim(email)),name,business,phone,created_at,created_at FROM leads WHERE id=NEW.lead_id
 ON CONFLICT(email) DO NOTHING;
 INSERT OR IGNORE INTO crm_deals(id,customer_id,lead_id,service,description,created_at,updated_at)
 SELECT l.id,c.id,l.id,NEW.service,l.goal,l.created_at,l.created_at FROM leads l JOIN crm_customers c ON c.email=lower(trim(l.email)) WHERE l.id=NEW.lead_id;
END;
INSERT INTO crm_customers(id,email,name,business,phone,created_at,updated_at)
 SELECT 'lead-'||id,lower(trim(email)),name,business,phone,created_at,created_at FROM leads WHERE status!='teste_tecnico' ORDER BY created_at
 ON CONFLICT(email) DO NOTHING;
INSERT OR IGNORE INTO crm_deals(id,customer_id,lead_id,service,description,created_at,updated_at)
 SELECT l.id,c.id,l.id,s.service,l.goal,l.created_at,l.created_at FROM leads l JOIN service_requests s ON s.lead_id=l.id JOIN crm_customers c ON c.email=lower(trim(l.email)) WHERE l.status!='teste_tecnico';

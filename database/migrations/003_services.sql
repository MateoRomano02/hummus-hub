CREATE TABLE services (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id  UUID NOT NULL REFERENCES agencies(id),
  client_id  UUID NOT NULL REFERENCES clients(id),
  type       TEXT NOT NULL,
  status     TEXT DEFAULT 'active',
  started_at DATE,
  config     JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

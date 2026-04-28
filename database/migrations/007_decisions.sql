CREATE TABLE decisions (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id       UUID NOT NULL REFERENCES agencies(id),
  client_id       UUID NOT NULL REFERENCES clients(id),
  campaign_id     UUID REFERENCES campaigns(id),
  source          TEXT,
  content         TEXT NOT NULL,
  context         TEXT,
  decided_by      TEXT,
  decided_at      TIMESTAMPTZ,
  is_reversal     BOOL DEFAULT false,
  reverses_id     UUID REFERENCES decisions(id),
  notion_block_id TEXT
);

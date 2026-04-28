CREATE TABLE content_items (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id         UUID NOT NULL REFERENCES agencies(id),
  client_id         UUID NOT NULL REFERENCES clients(id),
  campaign_id       UUID REFERENCES campaigns(id),
  type              TEXT NOT NULL,
  platform          TEXT,
  copy_text         TEXT,
  brief_context     TEXT,
  audit_notes       TEXT,
  designed_until    DATE,
  programmed_until  DATE,
  published_at      TIMESTAMPTZ,
  assigned_cm       TEXT,
  assigned_designer TEXT,
  status            TEXT DEFAULT 'planning',
  drive_file_id     TEXT,
  notion_block_id   TEXT,
  extra             JSONB DEFAULT '{}'
);
CREATE INDEX idx_content_dates ON content_items(client_id, designed_until, programmed_until);

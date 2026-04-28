CREATE TABLE brand_assets (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id      UUID NOT NULL REFERENCES agencies(id),
  client_id      UUID NOT NULL REFERENCES clients(id),
  asset_type     TEXT NOT NULL,
  label          TEXT,
  source         TEXT NOT NULL DEFAULT 'google_drive',
  drive_file_id  TEXT,
  drive_url      TEXT,
  r2_key         TEXT,
  r2_url         TEXT,
  external_url   TEXT,
  mime_type      TEXT,
  file_size_kb   INT,
  is_primary     BOOL DEFAULT false,
  meta           JSONB DEFAULT '{}',
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE meetings (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id             UUID NOT NULL REFERENCES agencies(id),
  client_id             UUID NOT NULL REFERENCES clients(id),
  date                  TIMESTAMPTZ NOT NULL,
  type                  TEXT,
  transcript_raw        TEXT,
  summary               TEXT,
  action_items          JSONB DEFAULT '[]',
  decisions_extracted   JSONB DEFAULT '[]',
  attendees             TEXT[] DEFAULT '{}',
  drive_recording_id    TEXT,
  notion_page_id        TEXT
);

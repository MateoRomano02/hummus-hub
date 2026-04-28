CREATE TABLE special_dates (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id            UUID NOT NULL REFERENCES agencies(id),
  name                 TEXT NOT NULL,
  date                 DATE NOT NULL,
  is_recurring         BOOL DEFAULT false,
  type                 TEXT,
  country              TEXT DEFAULT 'AR',
  relevant_industries  TEXT[] DEFAULT '{}',
  relevant_clients     UUID[] DEFAULT '{}',
  lead_time_days       INT DEFAULT 14,
  notes                TEXT,
  extra                JSONB DEFAULT '{}'
);

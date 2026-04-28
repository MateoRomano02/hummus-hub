CREATE TABLE team_members (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id             UUID NOT NULL REFERENCES agencies(id),
  name                  TEXT NOT NULL,
  role                  TEXT NOT NULL,
  email                 TEXT,
  is_external           BOOL DEFAULT false,
  skills                TEXT[] DEFAULT '{}',
  assigned_clients      UUID[] DEFAULT '{}',
  capacity_weekly_hours INT,
  meta                  JSONB DEFAULT '{}'
);

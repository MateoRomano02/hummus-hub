CREATE TABLE agent_logs (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id    UUID NOT NULL REFERENCES agencies(id),
  agent_type   TEXT NOT NULL,
  client_id    UUID REFERENCES clients(id),
  input_data   JSONB,
  output_data  JSONB,
  model_used   TEXT,
  tokens_in    INT,
  tokens_out   INT,
  cache_hit    BOOL,
  prompt_hash  TEXT,
  duration_ms  INT,
  status       TEXT,
  error_msg    TEXT,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_logs_agent_type ON agent_logs(agent_type, created_at DESC);
CREATE INDEX idx_logs_prompt     ON agent_logs(agent_type, prompt_hash);

ALTER TABLE clients        ENABLE ROW LEVEL SECURITY;
ALTER TABLE services       ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_assets   ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns      ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_items  ENABLE ROW LEVEL SECURITY;
ALTER TABLE decisions      ENABLE ROW LEVEL SECURITY;
ALTER TABLE meetings       ENABLE ROW LEVEL SECURITY;
ALTER TABLE metrics        ENABLE ROW LEVEL SECURITY;
ALTER TABLE special_dates  ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members   ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_logs     ENABLE ROW LEVEL SECURITY;

CREATE POLICY agency_isolation_clients ON clients
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_services ON services
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_brand_assets ON brand_assets
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_campaigns ON campaigns
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_content_items ON content_items
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_decisions ON decisions
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_meetings ON meetings
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_metrics ON metrics
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_special_dates ON special_dates
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_team_members ON team_members
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

CREATE POLICY agency_isolation_agent_logs ON agent_logs
  FOR ALL USING (agency_id = current_setting('app.current_agency_id')::UUID);

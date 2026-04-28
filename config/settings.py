from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str
    
    # Notion
    notion_api_key: str
    notion_db_clients: str
    notion_db_campaigns: str
    notion_db_content: str
    notion_db_decisions: str
    notion_db_metrics: str
    notion_db_assets: str
    notion_db_calendar: str
    notion_page_id: Optional[str] = None
    
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # Google Drive
    drive_service_account_json: Optional[str] = None
    
    # Notifications
    gmail_user: Optional[str] = None
    gmail_app_password: Optional[str] = None
    error_notify_email: Optional[str] = None
    
    # Multi-tenant
    default_agency_id: str
    
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra fields like GOOGLE_SERVICE_ACCOUNT_JSON if they exist
    )

settings = Settings()

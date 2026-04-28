from supabase import create_client, Client
from config.settings import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
supabase_admin: Client = create_client(settings.supabase_url, settings.supabase_service_key)

def set_agency_context(client: Client, agency_id: str):
    client.rpc('set_config', {
        'setting': 'app.current_agency_id',
        'value': agency_id
    }).execute()

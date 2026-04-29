from supabase import create_client, Client
from config.settings import settings

# Anon client for standard operations (respects RLS)
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

# Admin client for infrastructure and background tasks (bypasses RLS)
supabase_admin: Client = create_client(settings.supabase_url, settings.supabase_service_key)

def set_agency_context(client: Client, agency_id: str):
    """
    Sets the current agency ID in the Postgres session for RLS.
    """
    client.rpc('set_config', {
        'setting': 'app.current_agency_id',
        'value': agency_id
    }).execute()

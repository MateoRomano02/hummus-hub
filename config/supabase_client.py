import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

def get_supabase_client() -> Client:
    """
    Initializes and returns a Supabase client using environment variables.
    Uses SERVICE_ROLE_KEY to bypass RLS for administrative sync tasks.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
        
    return create_client(url, key)

# Shared client instance
supabase: Client = get_supabase_client()

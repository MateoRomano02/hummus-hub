from fastapi import APIRouter, BackgroundTasks
from integrations.notion_sync import sync_notion_to_supabase

from database.client import supabase_admin as supabase

router = APIRouter()

@router.post("/pull")
async def pull_all_from_notion(background_tasks: BackgroundTasks):
    """
    Manually triggers the Notion -> Supabase synchronization.
    Runs in the background.
    """
    background_tasks.add_task(sync_notion_to_supabase)
    return {"status": "sync_started", "message": "Pulling data from Notion in background."}

@router.post("/pull/{client_id}")
async def pull_client_from_notion(client_id: str, background_tasks: BackgroundTasks):
    """
    Triggers sync for a specific client by their Supabase ID.
    """
    try:
        # Fetch notion_page_id from Supabase to know which page to pull
        res = supabase.table("clients").select("notion_page_id").eq("id", client_id).single().execute()
        
        if not res.data or not res.data.get("notion_page_id"):
            return {"status": "error", "message": f"Client {client_id} not found or has no Notion Page ID linked."}
        
        notion_page_id = res.data["notion_page_id"]
        background_tasks.add_task(sync_notion_to_supabase, notion_page_id=notion_page_id)
        
        return {"status": "sync_started", "message": f"Pulling data for client {client_id} in background."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

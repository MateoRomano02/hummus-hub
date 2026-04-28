from fastapi import APIRouter, BackgroundTasks
from integrations.notion_sync import sync_notion_to_supabase

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
async def pull_client_from_notion(client_id: str):
    # This could be more specific, but for now we run the full sync
    background_tasks = BackgroundTasks()
    background_tasks.add_task(sync_notion_to_supabase)
    return {"status": "sync_started", "message": f"Pulling data for client {client_id} in background."}

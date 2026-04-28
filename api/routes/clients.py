from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from database.client import supabase_admin
from notion.sync import push_to_notion
from config.settings import settings

router = APIRouter()

class ClientOnboardRequest(BaseModel):
    name: str
    industry: str
    assigned_cm: str
    briefing_url: Optional[str] = None
    brand_manual_url: Optional[str] = None
    extra: Optional[Dict[str, Any]] = {}

@router.get("/")
async def list_clients():
    res = supabase_admin.table("clients").select("*").execute()
    return res.data

@router.get("/{client_id}")
async def get_client(client_id: str):
    res = supabase_admin.table("clients").select("*").eq("id", client_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Client not found")
    return res.data

@router.post("/onboard")
async def onboard_client(request: ClientOnboardRequest):
    """
    Onboards a new client through the API:
    1. Creates the record in Supabase.
    2. Syncs to Notion (Premium Layout).
    """
    data = request.dict()
    name = data.get("name")
    
    # Resolve Agency ID
    agencies = supabase_admin.table("agencies").select("id").limit(1).execute()
    agency_id = agencies.data[0]["id"] if agencies.data else settings.default_agency_id
    
    # Prepare Supabase payload
    supabase_data = {
        "name": name,
        "industry": data.get("industry"),
        "assigned_cm": data.get("assigned_cm"),
        "agency_id": agency_id,
        "slug": name.lower().replace(" ", "-"),
        "brand_manual_url": data.get("brand_manual_url"),
        "extra": {
            **(data.get("extra") or {}),
            "briefing_url": data.get("briefing_url")
        }
    }
    
    try:
        # 1. Insert into Supabase
        res = supabase_admin.table("clients").insert(supabase_data).execute()
        if not res.data:
            raise HTTPException(status_code=500, detail="Failed to create client in Supabase")
        
        new_client = res.data[0]
        client_id = new_client["id"]
        
        # 2. Sync to Notion
        notion_id = push_to_notion("client", client_id, new_client)
        
        if not notion_id:
            return {
                "status": "partial_success",
                "message": "Client created in database but Notion sync failed.",
                "client_id": client_id
            }
            
        clean_id = notion_id.replace("-", "")
        return {
            "status": "success",
            "message": f"Client {name} onboarded successfully",
            "client_id": client_id,
            "notion_url": f"https://www.notion.so/{clean_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

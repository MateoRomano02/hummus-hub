from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from database.client import supabase_admin
from notion.sync import push_to_notion
from config.settings import settings
import logging

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")
logger = logging.getLogger(__name__)

class PremiumOnboardRequest(BaseModel):
    name: str
    industry: str
    team: str = "Team Sofi & Ori"
    brand_voice: Optional[str] = ""
    target_audience: Optional[str] = ""
    value_prop: Optional[str] = ""
    instagram: Optional[str] = ""
    website: Optional[str] = ""
    briefing_url: Optional[str] = ""
    brand_manual_url: Optional[str] = ""

@router.get("/", response_class=HTMLResponse)
async def get_onboarding_form(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@router.post("/submit")
async def submit_onboarding(request: PremiumOnboardRequest):
    """
    Handles the premium onboarding form submission:
    1. Creates/Updates record in Supabase.
    2. Syncs to Notion with full Second Brain structure.
    """
    try:
        # Resolve Agency ID
        agencies = supabase_admin.table("agencies").select("id").limit(1).execute()
        agency_id = agencies.data[0]["id"] if agencies.data else settings.default_agency_id
        
        # Prepare data for Supabase
        client_data = {
            "name": request.name,
            "agency_id": agency_id,
            "slug": request.name.lower().replace(" ", "-"),
            "industry": request.industry,
            "team": request.team,
            "brand_voice": request.brand_voice,
            "target_audience": request.target_audience,
            "value_prop": request.value_prop,
            "instagram": request.instagram,
            "website": request.website,
            "briefing_url": request.briefing_url,
            "brand_manual_url": request.brand_manual_url,
            "status": "active"
        }
        
        # 1. Insert into Supabase
        res = supabase_admin.table("clients").insert(client_data).execute()
        if not res.data:
            raise HTTPException(status_code=500, detail="Error al guardar en base de datos")
            
        new_client = res.data[0]
        client_id = new_client["id"]
        
        # 2. Trigger Notion Sync (creates the page and sub-blocks)
        notion_id = push_to_notion("client", client_id, new_client)
        
        if not notion_id:
            return {
                "status": "partial_success",
                "message": "Cliente creado en DB pero falló sincronización con Notion.",
                "client_id": client_id
            }
            
        clean_id = notion_id.replace("-", "")
        return {
            "status": "success",
            "message": f"Cliente {request.name} cargado con éxito",
            "client_id": client_id,
            "notion_url": f"https://www.notion.so/{clean_id}"
        }
        
    except Exception as e:
        logger.error(f"Error in onboarding submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))

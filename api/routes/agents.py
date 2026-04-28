from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents.hee_agent import generate_email
from agents.decision_agent import extract_decisions

router = APIRouter()

class EmailRequest(BaseModel):
    client_id: str
    objective: str

class DecisionRequest(BaseModel):
    client_id: str
    text: str
    campaign_id: Optional[str] = None

@router.post("/hee/generate")
async def trigger_hee(request: EmailRequest):
    try:
        result = generate_email(request.client_id, request.objective)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decisions/extract")
async def trigger_decision_extraction(request: DecisionRequest):
    try:
        result = extract_decisions(request.client_id, request.text, request.campaign_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

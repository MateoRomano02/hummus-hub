from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
async def register_asset():
    # TODO: Implement asset registration to Supabase
    return {"message": "Asset registered"}

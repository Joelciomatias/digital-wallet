from fastapi import APIRouter

router = APIRouter()

@router.get("/balance")
async def get_balance():
    return {"message": "ok"}

@router.post("/event")
async def post_event():
    return {"message": "ok"}

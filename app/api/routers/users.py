from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_users():
    return {"message": "List of all users"}


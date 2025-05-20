from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.schemas.users import User
import app.services.user as service

router = APIRouter(prefix="/users", tags=["Users"])
limiter = Limiter(key_func=get_remote_address)
@router.post("/new_user")
@limiter.limit("3/minute", methods=["POST"])
async def add_user(user:User, request: Request):
    user_created = await service.add_user(user)
    if user_created:
        return {"status": "Пользователь создан"}
    else:
        return {"status": "Пользователь уже существует"}

@router.post("/delete_user")
async def delete_user(user:User):
    await service.delete_user(user)
    return { "status": "Пользователь удален"}
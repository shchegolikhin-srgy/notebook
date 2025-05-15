from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import app.crud.items as crud
from app.schemas.items import Task, UpdateTask
from app.schemas.token import Token, TokenData
from app.core.config import settings
from app.services.auth import create_access_token, decode_token
from app.services.redis import get_redis
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/items", tags=["Items"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/items/read_tasks")

@router.post("/delete_task")
async def delete_task(task:Task):
    await crud.delete_task(task)
    return { "status": "success"}

@router.post("/update_task")
async def update_task(task:UpdateTask):
    await crud.update_task(task)
    return { "status": "success"}

@router.get("/read_tasks")
async def read_tasks(token: str = Depends(oauth2_scheme), user: TokenData = Depends(decode_token)):
    print(user.username)
    tasks = await crud.get_tasks()
    return tasks

@router.post("/new_task")
async def add_task(task:Task):
    await crud.add_task(task)
    return { "status": "success"}

@router.post("/toggle_task")
async def toggle_complete_task(task:Task):
    await crud.toggle_complete_task(task)
    return { "status": "success"}

@router.get("/protected")
async def protected_route(current_user: TokenData = Depends(decode_token)):
    return {
        "message": f"Привет, {current_user.username}!",
        "status": "Доступ разрешён"
    }
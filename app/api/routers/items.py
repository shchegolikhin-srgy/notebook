from fastapi import APIRouter, Depends, HTTPException, Request
import app.crud.items as crud
from app.schemas.items import Task, UpdateTask, DeleteTask
from app.services.auth import  get_current_user
from app.schemas.users import User
from app.schemas.token import TokenData

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/delete_task")
async def delete_task(task:DeleteTask, token: TokenData = Depends(get_current_user)):
    await crud.delete_task(task= task, current_user = token)
    return { "status": "success"}

@router.post("/update_task")
async def update_task(task:UpdateTask, token: TokenData = Depends(get_current_user)):
    await crud.update_task(task= task, current_user = token)
    return { "status": "success"}

@router.get("/read_tasks")
async def read_tasks(token: TokenData = Depends(get_current_user)):
    tasks = await crud.get_tasks(token)
    return tasks

@router.post("/new_task")
async def add_task(task:Task, token: TokenData = Depends(get_current_user)):
    await crud.add_task(task=task, current_user = token)
    return { "status": "success"}

@router.post("/toggle_task")
async def toggle_complete_task(task:Task, token: TokenData = Depends(get_current_user)):
    await crud.toggle_complete_task(task=task, current_user = token)
    return { "status": "success"}

@router.get("/protected")
async def protected_route(token: TokenData = Depends(get_current_user)):
    return {
        "message": f"Привет, {token.username}!",
        "status": "Доступ разрешён"
    }
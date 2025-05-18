from fastapi import APIRouter, Depends, HTTPException, Request
import app.crud.items as crud
from app.schemas.items import Task, UpdateTask
from app.services.auth import  get_current_user
from app.schemas.users import User

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/delete_task")
async def delete_task(task:Task):
    await crud.delete_task(task)
    return { "status": "success"}

@router.post("/update_task")
async def update_task(task:UpdateTask):
    await crud.update_task(task)
    return { "status": "success"}

@router.get("/read_tasks")
async def read_tasks(current_user: User = Depends(get_current_user)):
    tasks = await crud.get_tasks(username=current_user.username)
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
async def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Привет, {current_user.username}!",
        "status": "Доступ разрешён"
    }
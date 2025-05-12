from fastapi import APIRouter, Depends, HTTPException
import app.crud.items as crud
from app.schemas.items import Task, UpdateTask

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
async def read_tasks(userId: int):
    response = await crud.get_tasks()
    return response

@router.post("/new_task")
async def add_task(task:Task):
    await crud.add_task(task)
    return { "status": "success"}

@router.post("/toggle_task")
async def toggle_complete_task(task:Task):
    await crud.toggle_complete_task(task)
    return { "status": "success"}

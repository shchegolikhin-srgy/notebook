from fastapi import APIRouter, Depends, HTTPException
import crud_items
from schemas_items import Task

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/delete_task")
async def deleteTask(task:Task):
    return "delete task"

@router.post("/update_task")
async def updateTask(task:Task):
    return "update"

@router.post("/read_tasks")
async def readTask(id: int):
    return "task"

@router.post("/new_task")
async def createTask(task:Task):
    crud_items.insertTask(task)
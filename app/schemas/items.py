from pydantic import BaseModel

class Task(BaseModel):
    text: str
    isCompleted: bool

class UpdateTask(BaseModel):
    text: str
    newText: str
    isCompleted: bool

class DeleteTask(BaseModel):
    text:str 
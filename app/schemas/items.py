from pydantic import BaseModel

class Task(BaseModel):
    text: str
    isCompleted: bool

class UpdateTask(BaseModel):
    text: str
    newText: str

class DeleteTask(BaseModel):
    text:str 
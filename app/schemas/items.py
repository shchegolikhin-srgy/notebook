from pydantic import BaseModel

class Task(BaseModel):
    userID: int
    text: str
    isCompleted: bool

class UpdateTask(BaseModel):
    userID: int
    text: str
    newText: str
    isCompleted: bool

class ReadTask(BaseModel):
    text: str
    isCompleted: bool
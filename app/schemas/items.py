from pydantic import BaseModel

class Task(BaseModel):
    userId: int
    text: str
    isCompleted: bool = False

class UpdateTask(BaseModel):
    userId: int
    text: str
    newText: str
    isCompleted: bool = False

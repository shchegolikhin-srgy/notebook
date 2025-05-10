from pydantic import BaseModel

class Task(BaseModel):
    userId: int
    text: str
    isCompleted: bool = False
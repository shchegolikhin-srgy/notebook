from pydantic import BaseModel

class Task(BaseModel):
    id: int
    text: str
    isCompleted: bool = False
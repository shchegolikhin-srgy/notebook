from pydantic import BaseModel

class User(BaseModel):
    id:int = -1
    username: str
    password: str
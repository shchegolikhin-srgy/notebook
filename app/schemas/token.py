from pydantic import BaseModel

class Token(BaseModel):
    access_token = ""
    token_type = "bearer"

class TokenData(BaseModel):
    username = None
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.routers.users import router as uRouter
from app.api.routers.items import router as iRouter
from app.db.base import connectionDB
from app.schemas.users import User

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.include_router(iRouter)
app.include_router(uRouter)

async def main():
    connectionDB()

#- - - - - http://127.0.0.1:8000/login - - - - - #

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth/data")
@limiter.limit("1/second", methods=["POST"])
async def auth(user: User, request: Request): ### request: Request !!!!!
    if user.username == "sergey" and user.password == "1234":
        return { "status": "success"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

#- - - - - http://127.0.0.1:8000 - - - - - #

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":  
    main()
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.routers.users import router as usersRouter
from app.api.routers.items import router as itemsRouter
from app.db.base import initialize_db_pool, close_db_pool, get_db_connection
from app.schemas.users import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start")
    await initialize_db_pool()
    yield
    await close_db_pool()
    print("Shutdown")

app = FastAPI(lifespan=lifespan)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.include_router(itemsRouter)
app.include_router(usersRouter)

#- - - - - http://127.0.0.1:8000/login - - - - - #

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#- - - - - http://127.0.0.1:8000 - - - - - #


# source .venv/bin/activate
# uvicorn app.main:app --reload 
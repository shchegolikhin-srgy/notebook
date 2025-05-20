from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.services.auth import  get_current_user
from app.api.routers import auth, users, items
from app.db.database import initialize_db_pool, close_db_pool, get_db_connection

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
app.include_router(items.router)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
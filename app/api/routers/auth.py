from fastapi import APIRouter, HTTPException, Request, status, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import User
import app.crud.users as crud
from app.schemas.token import Token
from app.core.config import settings
from app.services.auth import create_access_token, decode_token
from app.services.redis import get_redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
router = APIRouter(prefix="/auth", tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/token", response_model=Token)
@limiter.limit("3/minute", methods=["POST"])
async def login_for_access_token(request:Request, user:User):
    redis = await get_redis()
    isCurrentUser= await crud.check_user(user)
    if isCurrentUser ==False:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
    )
    accessTokenExpires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = await create_access_token(
        data={"sub": user.username}, expires_delta=accessTokenExpires
    )
    return {"access_token": accessToken, "token_type": "bearer"  }

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), user: dict = Depends(decode_token)):
    redis = await get_redis()
    await redis.delete(token)  
    return {"status": "success", "message": "Вы вышли из системы"}

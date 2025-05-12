from app.core.config import settings
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.schemas.token import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise JWTError
        return TokenData(username=username)
    except JWTError:
        raise JWTError("Could not validate credentials")
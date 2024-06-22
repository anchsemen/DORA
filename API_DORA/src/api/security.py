from typing import Union

from fastapi import HTTPException, Depends, status, Cookie
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from src.api.schemas import User

# Настройки JWT
SECRET_KEY = "YOUR_SECRET_KEY"
DEV_SECRET_KET = "TOP_SECRET_KEY"
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def create_access_token(user: User) -> str:
    data = user.model_dump()

    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Union[str, HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if type(token) != str:
        token = token.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return User(id=user_id,
                username=username)

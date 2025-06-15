from fastapi import Request, HTTPException, Cookie, Depends
from typing import Annotated
from starlette import status
from db import DataBase, User


async def get_database(request: Request) -> DataBase:
    return request.app.state.db

async def auth_user(auth: Annotated[str | None, Cookie()] = None, db = Depends(get_database)) -> User:
    if auth is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Укажите auth")
    
    user = db.auth_user_by_cookie(auth)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Куки не найден")
    
    return user

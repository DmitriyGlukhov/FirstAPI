from fastapi import APIRouter, Request, Response, Depends, HTTPException
from starlette import status
from dependencies import get_database, auth_user
from api_models import AuthData, ResponseUserData
from db import DataBase, User


router_user = APIRouter(prefix='/user', tags=['user'])


@router_user.post("/register")
async def register_user(
        response: Response,
        auth_data: AuthData,
        db: DataBase = Depends(get_database)
):
    user = db.create_user(auth_data.login, auth_data.password)
    if user is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    cookie = user.set_cookie()
    response.set_cookie(
        key='auth',
        value=cookie,
        httponly=True,
        secure=True,
        samesite='none',
        # domain='localhost'
    )
    return {"status": "ok"}


@router_user.post("/auth")
async def login_user(
    response: Response,
    auth_data: AuthData,
    db: DataBase = Depends(get_database)
):
    user = db.auth_user_by_login_pass(auth_data.login, auth_data.password)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    cookie = user.set_cookie()
    response.set_cookie(
        key='auth',
        value=cookie,
        httponly=True,
        secure=True,
        samesite='none',
        # domain='localhost'
    )
    return {"status": "ok"}


@router_user.post("/logout")
async def logout_user(
    response: Response,
    user: User = Depends(auth_user),
):
    user.unset_cookie()
    response.delete_cookie(key='auth')
    return {"status": "ok"}

@router_user.get("/")
async def get_user(
    user: User = Depends(auth_user)
):
    return ResponseUserData.model_validate(user.get_fields())
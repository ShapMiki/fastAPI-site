from fastapi import APIRouter, Response, Depends, Request

from users.schemas import SUser, SUserLogin
from users.dao import UsersDAO
from users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from users.dependencies import get_current_user

from exceptions import *

router = APIRouter(
    prefix="/auth",
    tags=["auth&users"],
)


@router.post("/register_api")
async def register(responce: Response, user_data: SUser):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    existing_user_passport_number = await UsersDAO.find_one_or_none(passport_number=user_data.passport_number)

    if existing_user or existing_user_passport_number:
        raise IncorrectEmailOrPassword

    hashed_password = get_password_hash(user_data.password)

    await UsersDAO.add_one(email=user_data.email, name=user_data.name, password=hashed_password, passport_number=user_data.passport_number)

    user = await UsersDAO.find_one_or_none(email=user_data.email)
    access_token = create_access_token(data={"sub": str(user.id)})
    responce.set_cookie(key="user_access_token", value=access_token, httponly=True)


@router.post("/login_api")
async def login(responce: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword

    access_token = create_access_token(data={"sub": str(user.id)})
    responce.set_cookie(key="user_access_token", value=access_token, httponly=True)


@router.post("/logout_api")
async def logout(responce: Response):
    responce.delete_cookie(key="user_access_token")



async def get_user_open_sourse(responce: Response,  user: SUser = Depends(get_current_user)):
    data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance
    }
    return data


"""@router.get('/personal_account')
async def  load_personal_account(request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    from main import templates

    data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance
    }
    return templates.TemplateResponse("personal_account.html", {"request": request, "data": data})
"""
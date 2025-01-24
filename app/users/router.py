from fastapi import APIRouter, Response, Depends, Request, Body

###########
from fastapi import  Form, File, UploadFile
from typing import Optional


from fastapi.responses import RedirectResponse

from users.schemas import *
from users.dao import UsersDAO
from users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from users.dependencies import get_current_user

from exceptions import *

router = APIRouter(
    prefix="/auth",
    tags=["auth&users"],
)


@router.post("/register_api")
async def register(responce: Response, user_data: SUserRegistrate):

    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise IncorrectEmailOrPassword

    hashed_password = get_password_hash(user_data.password)

    await UsersDAO.add_one(email=user_data.email, name=user_data.name, password=hashed_password, surname=user_data.surname)

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
async def logout(response: Response):
    return response.delete_cookie(key="user_access_token", path="/")

"""
@router.get("/logout_api")
async def logout(response: Response):
    return RedirectResponse(url="/", status_code=302)"""



@router.post('/update_user_info_api')
async def update_user_info(user_update: SUserUpdate = Body(...), user: SUser = Depends(get_current_user)):
    print(user_update.name, '\n')
    print(user_update.surname, '\n')
    print(user_update.telephone, '\n')
    print(user_update.description, '\n', '\n', '\n')

    await UsersDAO.update_one(user.id, **user_update.dict())



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
from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from pages.service import *

from users.schemas import SUser, SUserLogin, SUser_personal_info
from users.dependencies import get_current_user

from cars.dao import ActivCarsDAO, PropertyCarsDAO

from config import settings

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)


templates = Jinja2Templates(directory="templates")


@router.get('/')
async def show_index(request: Request, user: SUser = Depends(get_current_user)):

    if user:
        data = await get_all_data(user, False, False)
    else:
        data = {
            'user_data': None,
            'activ_lot_data': None,
            'property_data': None
        }

    return templates.TemplateResponse("index.html", {"request": request, 'data': data})


@router.get('/registrate')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("user/registrate_page.html", {"request": request, 'settings': {'web_path': settings.web_path}})


@router.get('/login')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("user/login_page.html", {"request": request, 'settings': {'web_path': settings.web_path}})


@router.get('/action_page')
async def redirect_action_page():
    return RedirectResponse(url="/pages/actions")
@router.get('/actions')
async def load_action_page(request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_data(user, True, False)

    return templates.TemplateResponse("lots/action_page.html", {"request": request, "data": data})




@router.get('/lot_load')
async def lot_load(request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user,True, False)

    return templates.TemplateResponse("lots/cars/lot_load_page.html", {"request": request, "data": data})


@router.get('/activ_lot_page/{lot_id}')
async def activ_lot_page(lot_id: int, request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_activ_lot_info(user, lot_id)

    if not data['activ_lot_data']:
        return RedirectResponse(url="/pages/action_page")

    return templates.TemplateResponse("lots/cars/action_lot_page.html", {"request": request, "data": data})


@router.get('/property_lot_page/{lot_id}')
async def property_lot_page(lot_id: int, request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_property_lot_info(user, lot_id)

    if not data['property_lot_data']:
        return RedirectResponse(url="/pages/personal_account")

    return templates.TemplateResponse("lots/cars/property_lot_page.html", {"request": request, "data": data})



@router.get('/stranger_account/{user_id}')
async def stranger_account(user_id: int, request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user,False, False)
    user_opensource_data = await get_stranger_data(user_id)

    if not user_opensource_data:
        raise HTTPException(status_code=404, detail="User not found")

    data['stranger'] = user_opensource_data

    return templates.TemplateResponse("user/communicate/stranger_personal_account_page.html", {"request": request, "data": data})


@router.get('/personal_account')
async def  load_personal_account(request: Request, responce: Response, user: SUser_personal_info = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user, True, True)

    return templates.TemplateResponse("user/personal_account_page.html", {"request": request, "data": data})


@router.get('/change_info_about_me')
async def change_info_about_me(request: Request, responce: Response, user: SUser_personal_info = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user, False, False)


    return templates.TemplateResponse("user/change_info_about_me_page.html", {"request": request, "data": data})


@router.get("/up_ballance")
async def load_up_ballance_page(request: Request, user: SUser = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_data(user, False, False)

    return templates.TemplateResponse("other/payments_page.html", {"request": request, "data": data})


@router.get("/chats")
async def load_chats_page(request: Request, user = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_users_chats_data(user)

    return templates.TemplateResponse("user/communicate/chats.html", {"request": request, "data": data})


@router.get("/chat/{chat_id}")
async def load_chat_page(chat_id: int, request: Request, user: SUser = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_user_chat_data(user, chat_id)
    return templates.TemplateResponse("user/communicate/chat_page.html", {"request": request, "data": data})

"""
@router.get('/main/{id}')
def show_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})

"""
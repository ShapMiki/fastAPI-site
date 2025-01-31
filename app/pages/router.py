from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from pages.service import *

from users.schemas import SUser, SUserLogin, SUser_personal_info
from users.dependencies import get_current_user

from cars.dao import ActivCarsDAO, PropertyCarsDAO

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)


templates = Jinja2Templates(directory="templates")


@router.get('/registrate')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("user/registrate_page.html", {"request": request})


@router.get('/login')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("user/login_page.html", {"request": request})


@router.get('/')
async def show_index(request: Request, user: SUser = Depends(get_current_user)):

    if user:
        user_data = {
            "name": user.name,
            "email": user.email,
            "ballance": user.ballance,
            "passport_number": user.passport_number
        }
        data={
            'user_data': user_data,
            'activ_lot_data': None,
            'property_data': None
        }
    else:
        data = {
            'user_data': None,
            'activ_lot_data': None,
            'property_data': None
        }

    return templates.TemplateResponse("index.html", {"request": request, 'data': data})


@router.get('/action_page')
async def redirect_action_page():
    return RedirectResponse(url="/pages/actions")

@router.get('/actions')
async def load_action_page(request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    data = await get_all_data(user, True, False)

    return templates.TemplateResponse("lots/action_page.html", {"request": request, "data": data})


"""
@router.get('/main/{id}')
def show_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})

"""

@router.get('/change_info_about_me')
async def change_info_about_me(request: Request, responce: Response, user: SUser_personal_info = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user, False, False)


    return templates.TemplateResponse("user/change_info_about_me_page.html", {"request": request, "data": data})


@router.get('/activ_lot_page/{lot_id}')
async def activ_lot_page(lot_id: int, request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    data = await get_activ_lot_info(user, lot_id)

    if not data['activ_lot_data']:
        return RedirectResponse(url="/pages/action_page")

    return templates.TemplateResponse("lots/cars/action_lot_page.html", {"request": request, "data": data})


@router.get('/property_lot_page/{lot_id}')
async def property_lot_page(lot_id: int, request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    data = await get_property_lot_info(user, lot_id)

    if not data['property_lot_data']:
        return RedirectResponse(url="/pages/personal_account")

    return templates.TemplateResponse("lots/cars/property_lot_page.html", {"request": request, "data": data})



@router.get('/lot_load')
async def lot_load(request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    data = await get_all_user_data(user,True, False)

    return templates.TemplateResponse("lots/cars/lot_load_page.html", {"request": request, "data": data})






@router.get('/personal_account')
async def  load_personal_account(request: Request, responce: Response, user: SUser_personal_info = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user, True, True)

    return templates.TemplateResponse("user/personal_account_page.html", {"request": request, "data": data})


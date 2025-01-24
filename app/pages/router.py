from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from pages.service import get_all_user_data

from users.schemas import SUser, SUserLogin, SUser_personal_info
from users.dependencies import get_current_user

from cars.dao import ActivCarsDAO, PropertyCarsDAO

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)


templates = Jinja2Templates(directory="templates")


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


@router.get('/registrate')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("user/registrate_page.html", {"request": request})

@router.get('/login')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("user/login_page.html", {"request": request})




@router.get('/actions/{action_type}')
def load_action_page(action_type: str, request: Request, responce: Response, user: SUser = Depends(get_current_user)):
    action_type,

    user_data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number
    }
    #реал получ данных

    if action_type == 'car':
        activ_lot_data = [{"ballance": user.ballance,
            "lot_start_date": "01.01.2025",
            "lot_end_date": "01.01.2026",
            "lot_number": 1,
            "lot_description":2,
            "lot_start_price":3,
            "lot_current_price":4,
            "lot_buy_price":5},
                          {"ballance": user.ballance,
                           "lot_start_date": "01.01.2025",
                           "lot_end_date": "01.01.2026",
                           "lot_number": 1,
                           "lot_description": 2,
                           "lot_start_price": 3,
                           "lot_current_price": 4,
                           "lot_buy_price": 5}
        ]

        data = {
            'user_data': user_data,
            'activ_lot_data': activ_lot_data,
            'property_data': None
        }

        return templates.TemplateResponse("lots/action_page.html", {"request": request, "data": data})
    elif action_type == 'gosnumbers':
        pass
    else:
        return RedirectResponse(url="/pages")

"""
@router.get('/main/{id}')
def show_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})

"""

@router.get('/change_info_about_me')
async def change_info_about_me(request: Request, responce: Response, user: SUser_personal_info = Depends(get_current_user)):

    if not user:
        return RedirectResponse(url="/pages/login")

    user_data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number,
        'surname': user.surname,
        'telephone': user.telephone,
        'registered_at': user.registered_at,
        'description': user.description
    }

    data = {
        'user_data': user_data,
        'activ_lot_data': None,
        'property_data': None
    }


    return templates.TemplateResponse("user/change_info_about_me_page.html", {"request": request, "data": data})





@router.get('/lot_load/{lot_name}')
async def lot_load(lot_name, request: Request, responce: Response, user: SUser = Depends(get_current_user)):

    user_data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number
    }


    data = {
        'user_data': user_data,
        'activ_lot_data': None,
        'property_data': None
    }

    if lot_name == 'car':
        return templates.TemplateResponse("lots/cars/lot_load_page.html", {"request": request, "data": data})
    elif lot_name == 'gosnumbers':
        return templates.TemplateResponse("lots/gosnumbers/lot_load_page.html", {"request": request, "data": data})
    else:
        return RedirectResponse(url="/pages")




@router.get('/personal_account')
async def  load_personal_account(request: Request, responce: Response, user: SUser_personal_info = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/pages/login")

    data = await get_all_user_data(user, True, True)

    return templates.TemplateResponse("user/personal_account_page.html", {"request": request, "data": data})


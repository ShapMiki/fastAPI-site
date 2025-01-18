from fastapi import APIRouter, Request, Depends, Response

from fastapi.templating import Jinja2Templates

from users.schemas import SUser, SUserLogin
from users.dependencies import get_current_user


router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)


templates = Jinja2Templates(directory="templates")


@router.get('/')
def show_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get('/registrate')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("registrate.html", {"request": request})

@router.get('/login')
def load_registrate_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/main/{id}')
def show_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})




@router.get('/personal_account')
async def  load_personal_account(request: Request, responce: Response, user: SUser = Depends(get_current_user)):
    data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance
    }
    return templates.TemplateResponse("personal_account.html", {"request": request, "data": data})


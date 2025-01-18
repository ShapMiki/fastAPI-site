from fastapi import APIRouter, Request, Depends
from sqlalchemy.sql import select

from modules.database import async_session_maker

from cars.models import Car
from cars.service import CarService
from cars.schemas import SCar

from users.dependencies import get_current_user
from users.schemas import SUserRegistrate


router = APIRouter(
    prefix="/cars",
    tags=["cars"],
)

@router.get("/")
async def get_car_info():
    result = await CarService.find_all()
    return result

@router.get("/get_user_cars_by_number/{number}")
async def get_car_info(number) -> SCar:
    result = await CarService.find_by_number(number)
    return result


@router.get("/get_my_ballance")
async def get_ballance(user: SUserRegistrate = Depends(get_current_user)):
    print(user.name)
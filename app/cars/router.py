from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.sql import select

from modules.database import async_session_maker

from cars.models import PropertyCars, ActivCars
from cars.dao import PropertyCarsDAO, ActivCarsDAO
from cars.schemas import SPropertyCars, SActivCars,  SUppPrice, SUpLoadActivCars

from users.dependencies import get_current_user
from users.schemas import SUser
from users.dao import UsersDAO

router = APIRouter(
    prefix="/cars",
    tags=["cars"],
)
"""
@router.get("/")
async def get_car_info():
    result = await CarService.find_all()
    return result
"""


@router.post("/add_activ_lot_api")
async def add_car(response: Response, car_data: SUpLoadActivCars, user: SUser = Depends(get_current_user)):
    car_data.owner = user.id
    car: SActivCars = ActivCars(**car_data.dict())
    await ActivCarsDAO.add_one(car)
    return RedirectResponse(url="/pages/personal_account", status_code=303)




async def transfer_activ_to_pasiv(data:SUppPrice, car_data: SActivCars, user: SUser):
    return 0
    old_owner = UsersDAO.find_by_id(car_data.owner)
    old_owner.ballance += data.price
    user.ballance -= data.price

    await UsersDAO.update_balance(old_owner.id, old_owner.ballance)
    await UsersDAO.update_balance(user.id, user.ballance)

    #ПЕРЕТАЩИТЬ АКТИВ В ПАСИВ
    pass


@router.post("/take_current_car_price_api")
async def register(responce: Response, data: SUppPrice, user: SUser = Depends(get_current_user) ):

    car_data = await ActivCarsDAO.find_by_id(data.car_id)
    if not car_data:
        raise HTTPException(status_code=404, detail="Car not found")

    if user.ballance < data.price:
        raise HTTPException(status_code=400, detail="Not enough money")

    if (car_data.current_price + car_data.price_step > data.price) and car_data.buy_price > data.price:
        raise HTTPException(status_code=400, detail="Price is too low")
    elif car_data.buy_price <= data.price:
        transfer_activ_to_pasiv(car_data, user)


    car_data.current_price = data.price
    car_data.current_owner = user.id

    await ActivCarsDAO.change_space(data.car_id, "current_price", data.price)



"""
@router.get("/get_user_cars_by_number/{number}")
async def get_car_info(number) -> SCar:
    result = await CarService.find_by_number(number)
    return result


@router.get("/get_my_ballance")
async def get_ballance(user: SUserRegistrate = Depends(get_current_user)):
    print(user.name)
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.sql import select

from modules.database import async_session_maker

from cars.models import PropertyCars, ActivCars
from cars.dao import PropertyCarsDAO, ActivCarsDAO
from cars.schemas import SPropertyCars, SActivCars, SUpLoadActivCars, SUppPrice
from cars.service import transfer_activ_to_pasiv

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

    return {'car_id': car.id}
    #return HTTPException(status_code=200, detail="Car added")


@router.post("/take_current_car_price_api/{car_id}")
async def register(responce: Response, car_id, data: SUppPrice, user: SUser = Depends(get_current_user) ):

    car_data = await ActivCarsDAO.find_by_id(int(car_id))

    if not car_data:
        raise HTTPException(status_code=404, detail="Car not found")

    if car_data.owner == user.id:
        raise HTTPException(status_code=400, detail="You can't buy your own car")

    if car_data.current_owner == user.id:
        raise HTTPException(status_code=400, detail="You already own this car")

    if user.ballance < data.price:
        raise HTTPException(status_code=400, detail="Not enough money")


    elif car_data.buy_price <= data.price and car_data.buy_price != 0:
        await transfer_activ_to_pasiv(data, car_data, user)
        return  RedirectResponse(url="/pages/personal_account", status_code=303)


    if (car_data.current_price + car_data.price_step > data.price or car_data.start_price > data.price) and not (car_data.current_price == car_data.start_price and data.price == car_data.start_price):
        raise HTTPException(status_code=400, detail="Price is too low")


    old_current_owner = await UsersDAO.find_by_id(car_data.current_owner)
    if car_data.current_owner:
        old_current_owner.ballance += car_data.current_price
        await UsersDAO.update_balance(old_current_owner.id, old_current_owner.ballance)

    user.ballance -= data.price
    car_data.current_price = data.price
    car_data.current_owner = user.id

    await UsersDAO.update_balance(user.id, user.ballance)
    await ActivCarsDAO.update_one_by_obj(car_data)



"""
@router.get("/get_user_cars_by_number/{number}")
async def get_car_info(number) -> SCar:
    result = await CarService.find_by_number(number)
    return result


@router.get("/get_my_ballance")
async def get_ballance(user: SUserRegistrate = Depends(get_current_user)):
    print(user.name)
"""
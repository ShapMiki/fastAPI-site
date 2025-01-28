from cars.schemas import SActivCars, SPropertyCars
from cars.models import ActivCars, PropertyCars
from cars.dao import PropertyCarsDAO, ActivCarsDAO

from users.schemas import SUser
from users.dao import UsersDAO


async def transfer_activ_to_pasiv(data, car_data, user: SUser):

    old_owner = await UsersDAO.find_by_id(car_data.owner)
    old_owner.ballance += data.price
    user.ballance -= data.price

    await UsersDAO.update_balance(old_owner.id, old_owner.ballance)
    await UsersDAO.update_balance(user.id, user.ballance)

    #еремещение из актив в приобретенные
    activ_car = car_data.to_dict()

    property_car = PropertyCars(
        id=activ_car['id'],
        ltype=activ_car['ltype'],
        name=activ_car['name'],
        description=activ_car['description'],
        owner=user.id,
        price=data.price
    )

    for key, value in activ_car.items():
        try:
            setattr(property_car, key, value)
        except AttributeError:
            pass

    setattr(property_car, 'owner', user.id)

    await PropertyCarsDAO.add_one(property_car)
    await ActivCarsDAO.delete_by_id(activ_car['id'])

"""from modules.database import async_session_maker
from sqlalchemy.sql import select

from cars.models import Car
from service.base import BaseService



class CarService(BaseService):
    model = Car

    @classmethod
    async def find_by_number(cls, number): #надо изменить
        async with async_session_maker() as session:
            query = select(Car).filter_by(car_number=number)
            cars = await session.execute(query)
            return cars.scalar_one_or_none()"""
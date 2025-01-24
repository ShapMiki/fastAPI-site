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
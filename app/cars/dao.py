from dao.base import BaseDAO
from modules.database import async_session_maker
from cars.models import PropertyCars, ActivCars
from sqlalchemy import select, insert
from datetime import datetime

class ActivCarsDAO(BaseDAO):
    model = ActivCars

    @classmethod
    async def find_by_owner(cls, owner: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(owner=owner)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def change_space(cls, id: int, space: str, value):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            obj = result.scalar_one_or_none()
            if obj:
                setattr(obj, space, value)
                await session.commit()
            return obj

    @classmethod
    async def update_one_by_obj(cls, obj):
        async with async_session_maker() as session:
            async with session.begin():
                await session.merge(obj)
                await session.commit()
                return obj

    @classmethod
    async def end_date_comparison(cls):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.end_date < datetime.now())
            result = await session.execute(query)
            return result.scalars().all()

class PropertyCarsDAO(BaseDAO):

    model = PropertyCars

    @classmethod
    async def find_by_owner(cls, owner: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(owner=owner)
            result = await session.execute(query)
            return result.scalars().all()


#ActivCarsDAO.change_space(1, "name", "new_name")
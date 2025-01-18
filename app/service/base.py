from modules.database import async_session_maker

from sqlalchemy.sql import select

class BaseService:
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            cars = await session.execute(query)
            return cars.scalars().all()

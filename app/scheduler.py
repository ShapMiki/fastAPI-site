from apscheduler.schedulers.asyncio import AsyncIOScheduler

from cars.dao import ActivCarsDAO, PropertyCarsDAO
from cars.models import PropertyCars

from users.dao import UsersDAO


class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def check_auctions(self):
        passed_end_date = await ActivCarsDAO.end_date_comparison()
        if not passed_end_date:
            return None

        for activ_car in passed_end_date:
            old_owner = await UsersDAO.find_by_id(activ_car.owner)

            if not activ_car.current_owner:
                await ActivCarsDAO.full_delete_by_id(activ_car.id)
                continue

            #old_current_owner = await UsersDAO.find_by_id(activ_car.current_owner)



            old_owner.ballance += activ_car.current_price
            #current_owner.ballance -= data.price       #Баланс должен уменьшаться при ставке

            await UsersDAO.update_balance(old_owner.id, old_owner.ballance)
            #await UsersDAO.update_balance(user.id, user.ballance)

            # еремещение из актив в приобретенные
            activ_car = activ_car.to_dict()

            property_car = PropertyCars(
                id=activ_car['id'],
                ltype=activ_car['ltype'],
                name=activ_car['name'],
                description=activ_car['description'],
                owner=activ_car['current_owner'],
                price=activ_car['current_price']
            )

            for key, value in activ_car.items():
                try:
                    setattr(property_car, key, value)
                except AttributeError:
                    pass

            setattr(property_car, 'owner', activ_car['current_owner'])


            await PropertyCarsDAO.add_one(property_car)
            await ActivCarsDAO.delete_by_id(activ_car['id'])


    def start(self):
        self.scheduler.add_job(self.check_auctions, 'interval', minutes=1)
        self.scheduler.start()
from cars.schemas import SActivCars, SPropertyCars
from cars.models import ActivCars, PropertyCars
from cars.dao import PropertyCarsDAO, ActivCarsDAO

from users.schemas import SUser
from users.dao import UsersDAO

from images.service import get_image_base64
import json


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


async def get_activ_data_list(lot_id:int = None, owner: int = None) -> dict:

    if lot_id:
        activ_lot_data = (await ActivCarsDAO.find_one_or_none(id=lot_id)).to_dict()
    elif owner:
        activ_lot_data = [car.to_dict() for car in await ActivCarsDAO.find_by_owner(owner)]
    else:
        activ_lot_data = [car.to_dict() for car in await ActivCarsDAO.find_all()]

    if not activ_lot_data:
        return None

    if len(activ_lot_data) == 0:
        return  None

    if lot_id:
        images = json.loads(activ_lot_data["images"])
        base64_images = []

        for image in images:
            base64_images.append(get_image_base64(f"cars/{image}"))
        activ_lot_data['images'] = base64_images

    else:
        for lot in activ_lot_data:
            images = json.loads(lot["images"])

            if len(images) == 0:
                image = None
            else:
                lot['image'] = get_image_base64(f"cars/{images[0]}")

    return activ_lot_data


async def get_property_data_list(lot_id: int = None, owner: int = None) -> dict:
    if lot_id:
        property_lot_data = (await PropertyCarsDAO.find_one_or_none(id=lot_id)).to_dict()
    elif owner:
        property_lot_data = [car.to_dict() for car in await PropertyCarsDAO.find_by_owner(owner)]
    else:
        property_lot_data = [car.to_dict() for car in await PropertyCarsDAO.find_all()]

    if not property_lot_data:
        return None

    if len(property_lot_data) == 0:
        return None

    if lot_id:
        images = json.loads(property_lot_data["images"])
        base64_images = []

        for image in images:
            base64_images.append(get_image_base64(f"cars/{image}"))
        property_lot_data['images'] = base64_images

    else:
        for lot in property_lot_data:
            images = json.loads(lot["images"])

            if len(images) == 0:
                image = None
            else:
                lot['image'] = get_image_base64(f"cars/{images[0]}")

    return property_lot_data



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
from users.schemas import SUser

from cars.dao import ActivCarsDAO, PropertyCarsDAO
from users.dao import UsersDAO

from config import settings

import base64


def get_user_image_base64(image_path):
    localisation_directory = f"{settings.image_scr}/users/{image_path}"
    try:
        with open(localisation_directory, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        return None

async def get_activ_lot_info(user: SUser, lot_id: int)->dict:
    data = {
        'user_data': None,
        'activ_lot_data': None,
        'another_data': None
    }


    user_data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number,
        'surname': user.surname,
        'telephone': user.telephone,
        'registered_at': user.registered_at,
        'description': user.description,
        'image_base64': get_user_image_base64(user.image)
    }


    activ_lot_data = await ActivCarsDAO.find_one_or_none(id=lot_id)

    if  activ_lot_data:
        activ_lot_data = activ_lot_data.to_dict()

        current_owner = await UsersDAO.find_one_or_none(id=activ_lot_data['current_owner'])
        if current_owner:
            activ_lot_data['current_owner'] = f"{current_owner.name} {current_owner.surname}"
        else:
            activ_lot_data['current_owner'] = activ_lot_data['owner']


        owner = await UsersDAO.find_one_or_none(id=activ_lot_data['owner'])
        another_data = {
            'owner': f"{owner.name} {owner.surname}",
        }
    else:
        another_data = None

    data['user_data'] = user_data
    data['activ_lot_data'] = activ_lot_data
    data['another_data'] = another_data

    return data




async def get_all_user_data(user: SUser, bool_activ_lots: bool, bool_property_lots: bool):
    data = {
        'user_data': None,
        'activ_lot_data': None,
        'property_data': None
    }

    user_data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number,
        'surname': user.surname,
        'telephone': user.telephone,
        'registered_at': user.registered_at,
        'description': user.description,
        'image_base64': get_user_image_base64(user.image)
    }

    data['user_data'] = user_data

    if bool_activ_lots:
        activ_lot_data = [car.to_dict() for car in await ActivCarsDAO.find_by_owner(user.id)]
        if len(activ_lot_data) == 0:
            activ_lot_data = None
        data['activ_lot_data'] = activ_lot_data

    if bool_property_lots:
        property_data = [car.to_dict() for car in await PropertyCarsDAO.find_by_owner(user.id)]
        if len(property_data) == 0:
            property_data = None
        data['property_data'] = property_data

    return data

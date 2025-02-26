from users.schemas import SUser

from cars.dao import ActivCarsDAO, PropertyCarsDAO
from cars.service import *

from users.dao import UsersDAO
from users.service import get_user_personal_info

from chat.dao import *
from chat.service import *

from config import settings
import json

from images.service import get_image_base64


async def get_activ_lot_info(user: SUser, lot_id: int)->dict:
    data = {
        'user_data': await get_user_personal_info(user),
        'activ_lot_data': None,
        'another_data': None
    }


    activ_lot_data = await get_activ_data_list(lot_id=lot_id)

    if activ_lot_data:
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

    data['activ_lot_data'] = activ_lot_data
    data['another_data'] = another_data

    return data

async def get_property_lot_info(user, lot_id):
    data = {
        'user_data': await get_user_personal_info(user),
        'property_lot_data': None,
        'another_data': None
    }

    property_data = await get_property_data_list(lot_id=lot_id)
    if property_data:
        owner = await UsersDAO.find_one_or_none(id=property_data['owner'])
        property_data['owner'] = f"{owner.name} {owner.surname}"
        data['property_lot_data'] = property_data


    return data

async def get_all_data(user: SUser, bool_activ_lots: bool, bool_property_lots: bool):
    data = {
        'user_data': await get_user_personal_info(user),
        'activ_lot_data': None,
        'property_lot_data': None
    }

    if bool_activ_lots:
        data['activ_lot_data'] = await get_activ_data_list()

    if bool_property_lots:
        data['property_data'] = await get_property_data_list()

    return data


async def get_all_user_data(user: SUser, bool_activ_lots: bool, bool_property_lots: bool):
    data = {
        'user_data': await get_user_personal_info(user),
        'activ_lot_data': None,
        'property_lot_data': None
    }

    if bool_activ_lots:
        data['activ_lot_data'] = await get_activ_data_list(owner=user.id)


    if bool_property_lots:
        data['property_lot_data'] = await get_property_data_list(owner=user.id)

    return data

async def get_users_chats_data(user):
    data = {
        'user_data': await get_user_personal_info(user, image=False),
        'chats_data': await ChatDAO.get_chats_list(user)
    }

    return data

async def get_user_chat_data(user: SUser, chat_id: int):
    data = {
        'user_data': await get_user_personal_info(user, image=False),
        'chats_data': await get_chat_data(user, chat_id)
    }
    return data
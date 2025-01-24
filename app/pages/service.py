from users.schemas import SUser

from cars.dao import ActivCarsDAO, PropertyCarsDAO


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
        'description': user.description
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

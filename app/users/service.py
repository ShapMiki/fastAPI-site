from fastapi import APIRouter, Depends
from fastapi.responses import Response

from users.dependencies import get_current_user
from users.schemas import SUser

from images.service import get_image_base64



async def get_user_open_sourse(user: SUser = Depends(get_current_user)):
    data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance
    }
    return data


async def get_user_personal_info(user: SUser = Depends(get_current_user)):
    data = {
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number,
        'surname': user.surname,
        'telephone': user.telephone,
        'registered_at': user.registered_at,
        'description': user.description,
        'image_base64': get_image_base64(f"users/{user.image}")
    }
    return data
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from users.dependencies import get_current_user
from users.schemas import SUser
from users.dao import UsersDAO

from config import settings

from images.service import get_image_base64

from datetime import timedelta


async def get_user_open_sourse(user_id: int, image: bool = True) -> dict:
    user = await UsersDAO.find_by_id(user_id)
    if not user:
        return None

    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "last_seance": (user.last_seance + timedelta(hours=settings.hour_zone)).strftime("%H:%M %d.%m.%Y"),
        "ballance": user.ballance
    }
    if image:
        data['image_base64'] = get_image_base64(f"users/{user.image}")


    return data


async def get_user_personal_info(user: SUser = Depends(get_current_user), image: bool = True):
    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "ballance": user.ballance,
        "passport_number": user.passport_number,
        'surname': user.surname,
        'telephone': user.telephone,
        'registered_at': (user.registered_at + timedelta(hours=settings.hour_zone)).strftime("%H:%M %d.%m.%Y"),
        "last_seance": (user.last_seance  + timedelta(hours=settings.hour_zone)).strftime("%H:%M %d.%m.%Y"),
        'description': user.description,
    }
    if image:
        data['image_base64'] = get_image_base64(f"users/{user.image}")

    return data
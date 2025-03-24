from sqlalchemy.orm import Session
#from users.schemas import Suser

from chat.models import *
from chat.dao import ChatDAO

from users.dao import UsersDAO

from images.service import get_image_base64

from config import settings
from exceptions import *

from datetime import datetime, timedelta



async def check_chat_user(user, chat):
    if user.id in [owner.id for owner in chat.owners]:
        raise True
    return False


async def get_chat_data(user, chat_id):
    chat = await ChatDAO.get_chat_data(user, chat_id=chat_id)
    if not chat:
        raise NotFound()
    if not check_chat_user(user, chat):
        raise Forbidden()

    #if user.id == chat.owners[0]:
       # secondary_user = chat.owners[1]
    #else:
     #   secondary_user = chat.owners[0]
    secondary_user = next(u for u in chat.owners if u.id != user.id)

    message_list = []
    for message in chat.messages:
        message_list.append({
                "id": message.id,
                "owner": message.owner,
                "text": message.text,
                "sending_date": (message.sending_date + timedelta(hours=settings.hour_zone)).strftime("%H:%M %d.%m.%Y"),
                "is_read": message.is_read
            })

    data = {
        'id': chat.id,
        'name': secondary_user.name,
        'image_base64': get_image_base64(f"users/{secondary_user.image}"),
        'created_at': chat.create_at,
        'message_list': message_list
    }

    difference = abs(secondary_user.last_seance - datetime.utcnow())
    if difference < timedelta(minutes=2):
        data['last_seance'] = "В сети 📱"
    elif difference < timedelta(days=1, hours=1):
        data['last_seance'] = "Был(-а) в сети в " + (secondary_user.last_seance + timedelta(hours=settings.hour_zone)).strftime("%H:%M")
    elif difference < timedelta(days=31):
        data['last_seance'] = "Был(-а) в сети " + (secondary_user.last_seance + timedelta(hours=settings.hour_zone)).strftime("%d.%m")
    else:
        data['last_seance'] = "Был(-а) в сети давно"

    return data

async def send_message(user, chat_id, message):
    chat = await ChatDAO.find_one_or_none_with_owners(id=chat_id)

    if not chat:
        raise NotFound()

    if not check_chat_user(user, chat):
        raise Fobridden()

    if chat:
        new_message = Message(
            chat_id=chat_id,
            owner=user.id,
            text=message,
            is_read= False,
            sending_date=datetime.utcnow(),
            chat=chat
        )
        await ChatDAO.create(new_message)


""" for chat in chat_list:
        if user.id == chat.owners[0]:
            secondary_user = await UsersDAO.find_one_or_none(id=chat.owners[1].id)
        else:
            secondary_user = await UsersDAO.find_one_or_none(id=chat.owners[0].id)
        chats_data.append({
            'id': chat.id,
            'name': secondary_user.name,
            'image_base64': get_image_base64(f"users/{secondary_user.image}"),
            'last_message': chat.last_message,
            'created_at': chat.create_at
        })

    return chats_data"""

"""{
            'id': 1,
            'name': 'Chat 1',
            'description': 'Description 1',
            'image': '',   #get_image_base64('chats/chat1.jpg')
            'last_message': 'ты козел'
        },"""
"""async def get_chat_data(user: SUser, chat_id: int):
    data = {
        'user_data': await get_user_personal_info(user),
        'chat_data': None
    }
    chat_data = await ChatsDAO.find_one_or_none(id=chat_id)
    if chat_data:
        data['chat_data'] = chat_data

    return data
"""


from sqlalchemy.orm import Session
#from users.schemas import Suser

from chat.models import *
from chat.dao import ChatDAO

from users.dao import UsersDAO

from images.service import get_image_base64

from datetime import datetime


async def create_chat(user1, user2):
    new_chat = Chat(
        owners=[user1, user2],
        create_at = datetime.now()
    )
    await ChatDAO.create(new_chat)

async def check_chat_user(user, chat_id):
    chat = await ChatDAO.find_one_or_none(id=chat_id)
    if user in chat.owners:
        return True
    return False

async def send_message(user, chat, message):
    chat = await ChatDAO.find_one_or_none(id=chat_id)
    if chat:
        new_message = Message(
            chat=chat,
            user=user,
            message=message,
            create_at=datetime.now()
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


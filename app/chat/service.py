
from users.schemas import Suser

from chat.models import *

async def create_chat():
    new_chat = Chat

async def get_chats_list(user):
    chats = user.chats
    print(chats)


async def get_chat_data(user: SUser, chat_id: int):
    data = {
        'user_data': await get_user_personal_info(user),
        'chat_data': None
    }
    chat_data = await ChatsDAO.find_one_or_none(id=chat_id)
    if chat_data:
        data['chat_data'] = chat_data

    return data



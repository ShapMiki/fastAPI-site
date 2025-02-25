from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from dao.base import BaseDAO
from modules.database import async_session_maker

from images.service import get_image_base64

from chat.models import Chat, Message

from users.models import Users



class ChatDAO(BaseDAO):
    model = Chat

    @classmethod
    async def get_chats_list(cls, user):
        async with async_session_maker() as session:
            user_with_chats = await session.execute(
                select(Users).options(selectinload(Users.chats).selectinload(Chat.owners)).filter_by(id=user.id)
            )
            user = user_with_chats.scalar_one_or_none()
            if not user:
                return []

            chat_list = user.chats
            chats_data = []

            for chat in chat_list:
                if user.id == chat.owners[0].id:
                    secondary_user = chat.owners[1]
                else:
                    secondary_user = chat.owners[0]
                chats_data.append({
                    'id': chat.id,
                    'name': secondary_user.name,
                    'image_base64': get_image_base64(f"users/{secondary_user.image}"),
                    'last_message': chat.last_message,
                    'created_at': chat.create_at
                })


            return chats_data

    @classmethod
    async def get_chat_data(cls, user, chat_id):
        async with async_session_maker() as session:
            chat = await session.execute(
                select(Chat).filter_by(id=chat_id).options(selectinload(Chat.messages))
            )
            print(chat)


class MessageDAO(BaseDAO):
    model = Message

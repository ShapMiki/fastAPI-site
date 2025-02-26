from sqlalchemy import select, insert, update, func
from sqlalchemy.orm import selectinload, joinedload
from dao.base import BaseDAO
from modules.database import async_session_maker
from datetime import datetime

from images.service import get_image_base64

from chat.models import Chat, Message

from users.models import Users



class ChatDAO(BaseDAO):
    model = Chat

    @classmethod
    async def find_one_or_none_with_owners(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs).options(selectinload(Chat.owners))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create_chat(cls, user1, user2):
        async with async_session_maker() as session:

            query = select(Chat).options(selectinload(Chat.owners)).where(
                Chat.owners.any(id=user1.id),
                Chat.owners.any(id=user2.id),
                func.array_length(Chat.owners, 1) == 2
            )
            existing_chat = await session.execute(query)
            existing_chat = existing_chat.scalar_one_or_none()

            if existing_chat:
                return existing_chat

            new_chat = Chat(
                owners=[user1, user2],
                create_at=datetime.utcnow()
            )
            await session.add(new_chat)
            await session.commit()
            return new_chat


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

                if chat.last_message:
                    last_message_data ={
                        'id': chat.last_message.id,
                        'owner': chat.last_message.owner.id,
                        'text': chat.last_message.text,
                        'sending_date': chat.last_message.sending_date,
                        'is_read': chat.last_message.is_read
                    }
                else:
                    last_message_data = None

                chats_data.append({
                    'id': chat.id,
                    'name': secondary_user.name,
                    'image_base64': get_image_base64(f"users/{secondary_user.image}"),
                    'last_message': last_message_data,
                    'created_at': chat.create_at
                })

            return chats_data


    @classmethod
    async def get_chat_data(cls, user, chat_id):
        async with async_session_maker() as session:
            chat = await session.execute(
                select(Chat)
                .filter_by(id=chat_id)
                .options(
                    selectinload(Chat.messages),
                    selectinload(Chat.owners)
                )
            )
            return chat.scalar_one_or_none()


class MessageDAO(BaseDAO):
    model = Message

from dao.base import BaseDAO
from chat.models import Chat, Message



class ChatDAO(BaseDAO):
    model = Chat


class MessageDAO(BaseDAO):
    model = Message

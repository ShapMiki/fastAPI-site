from dao.base import BaseDAO
from chat.modelss import Chat, Message



class ChatDAO(BaseDAO):
    model = Chat


class MessageDAO(BaseDAO):
    model = Message

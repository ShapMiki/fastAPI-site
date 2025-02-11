from sqlalchemy import Table, Column, Integer, ForeignKey
from modules.database import Base

chat_user_association = Table(
    'chat_user_association',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


chat_message_association = Table(
    'chat_message_association',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.id')),
    Column('message_id', Integer, ForeignKey('message.id'))
)
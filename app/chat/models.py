from sqlalchemy import Column, Integer, String, ForeignKey, Computed, Double, DateTime
from sqlalchemy.orm import relationship
from modules.database import Base
from association.associations import chat_user_association, chat_message_association


class Chat(Base):
    __tablename__ = 'chat'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    last_message_date = Column(DateTime)
    create_at = Column(DateTime)

    owners = relationship('Users', secondary=chat_user_association, back_populates='chats')
    messages_id = relationship('Message',secondary=chat_message_association, back_populates='chat_id')



class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    text = Column(String, nullable=False)

    sending_date = Column(DateTime)

    is_read = Column(String, default='False', nullable=False)

    chat_id = relationship("Chat", secondary=chat_message_association, back_populates='messages_id')




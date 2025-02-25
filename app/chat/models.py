from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from modules.database import Base
from association.associations import chat_user_association


class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    text = Column(String, nullable=False)
    sending_date = Column(DateTime)
    is_read = Column(String, default='False', nullable=False)

    chat = relationship('Chat', back_populates='messages', foreign_keys=[chat_id])



class Chat(Base):
    __tablename__ = 'chat'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    last_message_id = Column(Integer, ForeignKey('message.id'))
    create_at = Column(DateTime)

    last_message = relationship('Message', uselist=False, foreign_keys=[last_message_id])

    owners = relationship('Users', secondary=chat_user_association, back_populates='chats')

    # ЯВНО УКАЗЫВАЕМ foreign_keys
    messages = relationship('Message', back_populates='chat', foreign_keys=[Message.chat_id])

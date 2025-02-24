from sqlalchemy import Column, Integer, DateTime, String, Double, Computed, Date, ARRAY
from sqlalchemy.orm import relationship

from modules.database import Base
from association.associations import chat_user_association

from datetime import datetime

from chat.models import Chat

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, nullable=False)
    name  = Column(String, nullable=False)
    surname = Column(String)

    description = Column(String)

    telephone = Column(String)
    registered_at = Column(DateTime , default=datetime.utcnow(), nullable=False)
    last_seance = Column(DateTime, default=datetime.utcnow(), nullable=False)
    passport_number = Column(String, unique=True)

    password = Column(String, nullable=False)

    like_car_lots = Column(String, default='[]', nullable=False)

    like_property_cars = Column(String, default='[]', nullable=False)

    last_lot_time = Column(DateTime, default=datetime.utcnow(), nullable=False) #время последнего лота, чтобы не было спама

    verefy_email = Column(String, default='False', nullable=False)
    verefy_passport = Column(String, default='False', nullable=False)

    ballance = Column(Double, default=0,  nullable=False)
    image = Column(String, default='none_user_photo.jpg')

    chats = relationship('Chat', secondary=chat_user_association, back_populates='owners')

"""class Property(Base):
    __tablename__ = 'property'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    buy_date = Column(Date, nullable=False)
    general_description = Column(String)
"""

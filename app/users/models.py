from sqlalchemy import Column, Integer, String, Double, Computed, Date, ARRAY
from modules.database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, nullable=False)
    name  = Column(String, nullable=False)
    surname = Column(String)

    description = Column(String)

    telephone = Column(String)
    registered_at = Column(Date , default=datetime.utcnow(), nullable=False)
    last_seance = Column(Date, default=datetime.utcnow(), nullable=False)
    passport_number = Column(String, unique=True)

    password = Column(String, nullable=False)

    like_car_lots = Column(String, default='[]', nullable=False)

    like_property_cars = Column(String, default='[]', nullable=False)

    #last_lot_time = Column(Date, default=datetime.utcnow(), nullable=False) #время последнего лота, чтобы не было спама

    verefy_email = Column(String, default='False', nullable=False)
    verefy_passport = Column(String, default='False', nullable=False)

    ballance = Column(Double, default=0,  nullable=False)
    image = Column(String, default='none_user_photo.jpg')

    chat_list = Column(ARRAY(Integer))

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

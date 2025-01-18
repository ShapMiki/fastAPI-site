from sqlalchemy import Column, Integer, String, ForeignKey, Date, Computed
from modules.database import Base

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    user_number = Column( String, ForeignKey('users.passport_number'), nullable=False, )
    brand = Column(String, nullable=False)
    body = Column(String, nullable=False)
    car_number = Column(String, nullable=False)
    buy_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    tax = Column(Integer, Computed('price*0.05'))
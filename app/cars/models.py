from sqlalchemy import Column, Integer, String, ForeignKey, Computed, Double, DateTime
from modules.database import Base

"""class Car():
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    user_number = Column( String, ForeignKey('users.passport_number'), nullable=False, )
    brand = Column(String, nullable=False)
    body = Column(String, nullable=False)
    car_number = Column(String, nullable=False)
    buy_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    tax = Column(Integer, Computed('price*0.05'))
"""
class ActivCars(Base):
    __tablename__ = 'activ_cars'
    __table_args__ = {'extend_existing': True}

    ltype = Column(String, default="cars", nullable=False)

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    brand = Column(String)
    model = Column(String)
    body = Column(String)

    fuel_type = Column(String)
    engine_volume = Column(Double)
    power = Column(Double)
    year = Column(Integer)
    gear_type = Column(String)
    range = Column(Double) #пробег

    current_owner = Column(Integer, ForeignKey('users.id'))
    start_price = Column(Double,  default=0, nullable=False)
    current_price = Column(Double, default=0, nullable=False)
    buy_price = Column(Double, default=float('inf'), nullable=False)
    price_step = Column(Double, default=float(0), nullable=False)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    registration = Column(String)
    images = Column(String, default='[]', nullable=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ltype': self.ltype,
            'owner': self.owner,
            'brand': self.brand,
            'model': self.model,
            'body': self.body,
            'fuel_type': self.fuel_type,
            'engine_volume': self.engine_volume,
            'power': self.power,
            'year': self.year,
            'gear_type': self.gear_type,
            'range': self.range,
            'current_owner': self.current_owner,
            'start_price': self.start_price,
            'current_price': self.current_price,
            'buy_price': self.buy_price,
            'price_step': self.price_step,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'registration': self.registration,
            'images': self.images
        }


class PropertyCars(Base):
    __tablename__ = 'property_cars'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    ltype = Column(String, default="cars", nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    brand = Column(String)
    model = Column(String)
    body = Column(String)

    fuel_type = Column(String)
    engine_volume = Column(Double)
    power = Column(Double)
    year = Column(Integer)
    gear_type = Column(String)

    range = Column(Double) #пробег

    price = Column(Double)

    buy_date = Column(DateTime)

    registration = Column(String)
    images =  Column(String, default='[]', nullable=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner,
            'brand': self.brand,
            'model': self.model,
            'body': self.body,
            'fuel_type': self.fuel_type,
            'engine_volume': self.engine_volume,
            'power': self.power,
            'year': self.year,
            'gear_type': self.gear_type,
            'range': self.range,
            'price': self.price,
            'buy_date': self.buy_date,
            'registration': self.registration,
            'images': self.images
        }

from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Optional
from config import settings

"""class SCar(BaseModel):
    id: int
    user_number: str
    brand: str
    body: str
    car_number: str
    buy_date: date
    price: int
    tax: int

    class Config:
        orm_mode = True"""

class SActivCars(BaseModel):
    id: int
    ltype: str
    name: str
    description: str
    owner: str
    brand: Optional[str] = None
    model: Optional[str] = None
    body: Optional[str] = None
    fuel_type: Optional[str] = None
    engine_volume: Optional[float] = None
    power: Optional[float] = None
    gear_type: Optional[str] = None
    year: Optional[int] = None
    range: Optional[float] = None
    current_owner: Optional[str] = None
    start_price: Optional[float] = None
    current_price: Optional[float] = None
    buy_price: Optional[float] = None
    price_step: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration: Optional[str] = None
    images: str = '[]'

    class Config:
        orm_mode = True


class SPropertyCars(BaseModel):
    id: int
    ltype: str
    name: str
    description: str
    owner: int
    brand: Optional[str] = None
    model: Optional[str] = None
    body: Optional[str] = None
    fuel_type: Optional[str] = None
    engine_volume: Optional[float] = None
    power: Optional[float] = None
    gear_type: Optional[str] = None
    year: Optional[int] = None
    range: Optional[float] = None
    price: Optional[float] = None
    buy_date: Optional[date] = None
    registration: Optional[str] = None
    images: str = '[]'

    class Config:
        orm_mode = True



class SUpLoadActivCars(BaseModel):
    ltype: str = Field(default='car')
    name: str
    description: str
    owner: str = Field(default='0')

    brand: Optional[str] = Field(default="Самоделка")
    model: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    fuel_type: Optional[str] = Field(default=None)
    engine_volume: Optional[float] = Field(default=None)
    power: Optional[float] = Field(default=None)
    gear_type: Optional[str] = Field(default=None)
    year: Optional[int] = Field(default=None)
    range: Optional[float] = Field(default=0)
    current_owner: Optional[str] = Field(default=None)

    start_price:Optional[float] = Field(default=0, ge=0)
    current_price: Optional[float] = Field(default=0)
    buy_price: Optional[float] = Field(default=0, ge=0)
    price_step: Optional[float] = Field(default=1)

    start_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    start_time: Optional[str] = Field(default="00:00:00")
    end_date: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=1))
    end_time: Optional[str] = Field(default="01:00:00")

    registration: Optional[str] = Field(default="Не указано")
    images: str = Field(default='[]')

    @field_validator('start_date', 'end_date', mode='before')
    def parse_dates(cls, value):
        if isinstance(value, str):
            for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', '%d.%m.%Y', '%Y.%m.%d'):
                try:
                    return (datetime.strptime(value, fmt).date() - timedelta(hours=settings.hour_zone))
                except ValueError:
                    continue
            return None

    @field_validator('start_price', 'buy_price', 'price_step', mode='before')
    def validate_prices(cls, value, field):
        if isinstance(value, str):
            try:
                value = float(value)
                if value < 0:
                    value = -value
            except ValueError:
                value = None
        return value

    @field_validator('*', mode='before')
    def validate_fields(cls, value, field):
        if isinstance(value, str) and value == "":
            value = None
        return value

    @model_validator(mode='after')
    def combine_date_time(cls, values):
        if values.start_date and values.start_time:
            values.start_date = datetime.combine(values.start_date,
                                                 datetime.strptime(values.start_time, '%H:%M').time())
        elif values.start_time:
            values.start_date = datetime.utcnow()
            values.start_date = datetime.combine(values.start_date, datetime.strptime(values.start_time, '%H:%M').time())
        elif not values.start_date:
            values.start_date = datetime.utcnow() - timedelta(hours=settings.hour_zone)

        if values.end_date and values.end_time:
            values.end_date = datetime.combine(values.end_date, datetime.strptime(values.end_time, '%H:%M').time())
        elif values.end_time:
            values.end_date = values.start_date + timedelta(days=1)
            values.end_date = datetime.combine(values.end_date, datetime.strptime(values.end_time, '%H:%M').time())
        elif not values.end_date:
            values.end_date = values.start_date + timedelta(days=1)

        if values.start_date:
            if values.start_date < datetime.utcnow():
                values.start_date = datetime.utcnow()


        if values.end_date:
            if values.end_date < datetime.utcnow():
                values.end_date = datetime.utcnow() + timedelta(days=1)


        if values.start_date and values.end_date:
            if values.end_date < values.start_date:
                values.end_date = values.start_date + timedelta(days=1)
            if (values.end_date - values.start_date).days > 31:
                values.end_date = values.start_date + timedelta(days=31)

        del values.start_time
        del values.end_time

        if values.buy_price and values.start_price:
            if values.start_price > values.buy_price:
                values.buy_price = 0

        values.start_date = values.start_date.replace(second=0, microsecond=0)
        values.end_date = values.end_date.replace(second=0, microsecond=0)
        return values


    class Config:
        orm_mode = True




class SUppPrice(BaseModel):
    price: float
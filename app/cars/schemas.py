from pydantic import BaseModel
from datetime import date

class SCar(BaseModel):
    id: int
    user_number: str
    brand: str
    body: str
    car_number: str
    buy_date: date
    price: int
    tax: int

    class Config:
        orm_mode = True
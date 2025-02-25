from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, Form

class SUser(BaseModel):
    id: int
    email: str
    ballance: float

    class Config:
        orm_mode = True

class SUserUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    surname: Optional[str] = Field(None, min_length=1, max_length=50)
    telephone: Optional[str] = Field(None)
    description: Optional[str] = Field(None, max_length=3000)

    class Config:
        orm_mode = True


class SUser_personal_info(BaseModel):
    email: EmailStr
    name: str
    surname: str
    passport_number: str
    registered_at: datetime
    telephone: str
    balance: float
    description: str
    have_cars_lots: list
    have_gosnumbers_lots: list
    property_cars: list
    property_gosnumbers: list

    class Config:
        orm_mode = True

class SUser_open_sourse(BaseModel):
    email: EmailStr
    name: str
    surname: str
    telephone: str
    balance: float
    description: str
    have_cars_lots: list
    have_gosnumbers_lots: list
    property_cars: list
    property_gosnumbers: list

    class Config:
        orm_mode = True


class SUserRegistrate(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str


    class Config:
        orm_mode = True


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    email: EmailStr
    password: str
    name: str
    passport_number: str
    balance: float

    class Config:
        orm_mode = True


class SUserRegistrate(BaseModel):
    email: EmailStr
    password: str
    name: str
    passport_number: str

    class Config:
        orm_mode = True


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
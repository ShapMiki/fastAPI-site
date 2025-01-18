from sqlalchemy import Column, Integer, String, Double
from modules.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name= Column(String, nullable=False)
    password= Column(String, nullable=False)
    passport_number= Column(String, unique=True, nullable=False)
    ballance = Column(Double, default=0,  nullable=False)
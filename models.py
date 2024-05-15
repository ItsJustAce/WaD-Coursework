from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True)
    phone_number = Column(Integer, unique=True)
    hashed_password = Column(String(255))
    username = Column(String(80), unique=True)


from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from db import Base


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    last_name = Column(String)
    pets = Column(String)
    location = Column(String)
    description = Column(String)

class House(Base):
    __tablename__ = 'Houses'
    house_id = Column(Integer, primary_key=True)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    available = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('Users.user_id'))


class UserApplication(Base):
    __tablename__ = 'User_applications'
    user_application_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    house_id = Column(Integer, ForeignKey('Houses.house_id'))

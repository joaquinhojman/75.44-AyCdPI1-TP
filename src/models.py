from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from db import Base


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    country = Column(String)
    age = Column(Integer)
    description = Column(String)
    photo_url = Column(String)


class House(Base):
    __tablename__ = 'Houses'
    house_id = Column(Integer, primary_key=True)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    available = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('Users.user_id'))
    rooms = Column(Integer)
    city = Column(String)
    image1 = Column(String)
    image2 = Column(String)
    image3 = Column(String)
    image4 = Column(String)
    image5 = Column(String)


class UserApplication(Base):
    __tablename__ = 'User_applications'
    user_application_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    house_id = Column(Integer, ForeignKey('Houses.house_id'))
    accepted = Column(Boolean, default=None)

class Pet(Base):
    __tablename__ = 'Pet'
    pet_id = Column(Integer, primary_key=True)
    animal_id = Column(String, ForeignKey('Animal.animal_id'))
    house_id = Column(Integer, ForeignKey('Houses.house_id'))
    pet_cant = Column(Integer)

class Animal(Base):
    __tablename__ = 'Animal'
    animal_id = Column(String, primary_key=True)


class Ratings(Base):
    __tablename__ = 'Ratings'

    user_id = Column(String, primary_key=True)
    house_id = Column(String, primary_key=True)
    rating = Column(Integer)
    comment = Column(String)

class RatingsHouses(Base):
    __tablename__ = 'RatingsHouses'

    user_id = Column(String, primary_key=True)
    house_id = Column(String, primary_key=True)
    rating = Column(Integer)
    comment = Column(String)

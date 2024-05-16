from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True)
    phone_number = Column(Integer, unique=True)
    hashed_password = Column(String(255))
    username = Column(String(80), unique=True)


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    capacity = Column(Integer)
    peak = Column(Integer)
    off_peak = Column(Integer)

class RoomType(Base):
    __tablename__ = 'room_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    max_occupancy = Column(Integer)

# class Hotel(Base):
#     __tablename__ = 'hotels'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True)
#     city_id = Column(Integer, ForeignKey('cities.id'))
#     city = relationship(City)

# class Room(Base):
#     __tablename__ = 'rooms'

#     id = Column(Integer, primary_key=True)
#     hotel_id = Column(Integer, ForeignKey('hotels.id'))
#     room_type_id = Column(Integer, ForeignKey('room_types.id'))
#     # hotel = relationship(Hotel)
#     room_type = relationship(RoomType)

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Replace 'users' with your user model table name
    city_id = Column(Integer, ForeignKey('cities.id'))
    # room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in = Column(Date)
    check_out = Column(Date)
    num_guests = Column(Integer)
    cancellation_charges = Column(Float)
    discount = Column(Float)
    total_price = Column(Float)
    is_cancelled = Column(Boolean, default=False)
    # hotel = relationship(Hotel)
    # room = relationship(Room)

class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    #rooms = relationship(Room)  # ManyToMany relationship

# features_rooms = Table('features_rooms',
#     Base.metadata,
#     Column('feature_id', Integer, ForeignKey('features.id')),
#     Column('room_id', Integer, ForeignKey('rooms.id'))
# )

# class Currency(Base):
#     __tablename__ = 'currencies'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(10))
#     # Add fields for exchange rates or methods to calculate based on another currency

# class Price(Base):
#     __tablename__ = 'prices'

#     id = Column(Integer, primary_key=True)
#     season = Column(String(20), Enum('peak', 'off-peak'))
#     currency_id = Column(Integer, ForeignKey('currencies.id'))
#     room_type_id = Column(Integer, ForeignKey('room_types.id'))
#     amount = Column(Float)  # Price per night
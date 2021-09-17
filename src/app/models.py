from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, )
    distance = Column(Integer)
    hours = Column(Integer)


class BoardingPasses(Base):
    __tablename__ = 'boarding_passes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    destination = Column(String, )
    address = Column(String, )
    boarding_datetime = Column(String, )
    checked_in = Column(Boolean, default=False)
    code = Column(String, )
    checked_at = Column(DateTime(timezone=True))

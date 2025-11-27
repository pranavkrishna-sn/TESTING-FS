from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImplementUserAuthentication(Base):
    __tablename__ = 'implement_user_authentication'
    id = Column(Integer, primary_key=True)
    name = Column(String)
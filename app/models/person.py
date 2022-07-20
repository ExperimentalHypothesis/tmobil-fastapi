
from ..database import Base
from sqlalchemy import Column, String, DateTime

class Person(Base):
    __abstract__ = True

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    dob = Column(DateTime, nullable=True)

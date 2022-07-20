
from ..database import Base
from sqlalchemy import Column, String, Integer

class Company(Base):
    __abstract__ = True

    ico = Column(Integer, nullable=True)
    dic = Column(String, nullable=True)

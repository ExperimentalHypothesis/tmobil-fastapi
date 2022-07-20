from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String, text)
from sqlalchemy.orm import relationship
from .company import Company
from .person import Person

class Customer(Company, Person):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


from ..database import Base
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String, Float, Table, text)
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    internal_id = Column(Integer, nullable=False) 
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.internal_id", ondelete="CASCADE"), nullable=False)
    order = relationship("Order")    
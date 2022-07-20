from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, Float, text)
from sqlalchemy.orm import relationship

from ..database import Base

class Order(Base):
    __tablename__ = "orders"
    
    internal_id = Column(Integer, primary_key=True)
    total_cost = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    customer = relationship("Customer")

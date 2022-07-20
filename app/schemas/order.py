from typing import List
from pydantic import BaseModel, conlist
from datetime import datetime
from .item import ItemReq, ItemResp

class OrderReq(BaseModel):
    """ Schema for accepting order posts requests. """
    total_cost: float
    customer_id: int 
    items: conlist(ItemReq, min_items=1) # there is no such order that has 0 items in it


class OrderResp(BaseModel):
    """ Schema that will be sent back to the caller when  getting all orders. """
    internal_id: int
    total_cost: float
    customer_id: int
    created_at: datetime
    
    class Config:
        orm_model: True

class OrderRespDetail(OrderResp):
    """ Schema that will be sent back to the caller when viewing order detail (GET order by id, or GET customer by id). """
    items: List[ItemResp]


    

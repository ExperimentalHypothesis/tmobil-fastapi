from typing import Union
from pydantic import BaseModel

class ItemReq(BaseModel):
    """ Schema for creating items """
    internal_id: int # each item has its special internal id (eg. piano = 10, flute = 11, drums = 12)
    price: float
    description: str
    order_id: Union[int, None] = None # this will be taken automatically from "internal_id" field when creating order
    
class ItemResp(BaseModel):
    """ Schema for sending back to caller """
    id: int
    description: str
    price: float
    internal_id: int
    order_id: int
    
    class Config:
        orm_mode = True
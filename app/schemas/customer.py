from typing import List, Union
from pydantic import EmailStr, validator, BaseModel
from datetime import datetime
from .company import Company
from .person import Person
from .order import OrderRespDetail

class CustomerReq(Person, Company):
    """ Schema that is to be followed for requests. All customers must have phone and email """
    phone: int
    email: EmailStr



class CustomerRespBasic(BaseModel):
    """ Schema that will be sent back in for get all customers. """
    id: int
    ico: Union[None, int] = None
    dic: Union[None, str] = None
    first_name: Union[None, str] = None
    last_name: Union[None, str] = None
    dob: Union[None, datetime] = None
    phone: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
    
class CustomerRespDetail(CustomerRespBasic):
    """ Schema that will be sent back in for get customer by id. """
    orders: Union[None, List[OrderRespDetail]] = None

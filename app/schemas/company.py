from pydantic import BaseModel


class Company(BaseModel):
    """ Base class to be subclassed by CustomerReq class """
    ico: int = None
    dic: str = None
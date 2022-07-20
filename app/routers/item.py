from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from ..schemas.item import ItemReq, ItemResp
from ..models.item import Item
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items")

@router.get("/", status_code=200, response_model=List[ItemResp])
def get_item(db: Session = Depends(get_db)):
    """ Get all items """
    items = db.query(Item).all()
    return items


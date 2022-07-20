from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from ..database import get_db
from ..schemas.order import OrderReq, OrderResp, OrderRespDetail
from ..models.order import Order
from ..models.item import Item
from sqlalchemy.orm import Session


router = APIRouter(prefix="/orders")

@router.get("/", response_model=List)
def get_orders(db: Session = Depends(get_db)):
    """ Get all orders. """
    orders = db.query(Order).all()
    print(orders)
    return orders

@router.get("/{order_id}", response_model=OrderRespDetail)
def get_orders(order_id: int, db: Session = Depends(get_db)):
    """ Get one order by id. """
    # select * from orders left join items on orders.internal_id = items.order_id where orders.internal_id = {order_id}
    result = db.query(Order, Item).join(Item, Item.order_id == Order.internal_id, isouter=True).filter(Item.order_id == order_id).all() 
    if result:
        ret_val = {}
        ret_val["internal_id"] = result[0].Order.internal_id
        ret_val["total_cost"] = result[0].Order.total_cost
        ret_val["customer_id"] = result[0].Order.customer_id
        ret_val["created_at"] = result[0].Order.created_at
        ret_val["items"] = [i.Item for i in result]
        return ret_val
    raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")

@router.post("/", status_code=201)
def create_order(payload: OrderReq, db: Session = Depends(get_db)):
    """ Create a new order. """    
    order = payload.dict()
    items = order.pop("items")
    new_order = Order(**order)
    db.add(new_order) 
    db.flush()

    new_items = []
    for item in items:
        item["order_id"] = new_order.internal_id # assign FK to PK of this new order
        new_items.append(Item(**item))

    db.add_all(new_items)
    db.commit()

    return payload.dict()

@router.put("/{order_id}", status_code=204, response_class=Response)
def update_order(order_id: int, payload: OrderReq, db: Session = Depends(get_db)):
    """ Update order with its nested items inside. 
        SQLAlchemy cannot do update in joint tables so I need to query orders and items separately.
        The simplest way is to drop the old items and create the new updated ones.
     """
    order_qry = db.query(Order).filter(Order.internal_id == order_id)
    order = order_qry.first()
    if order:
        # update the order
        order = payload.dict()
        updated_items = order.pop("items")
        order_qry.update(order)

        # drop the old and create the new
        db.query(Item).filter(Item.order_id == order_id).delete(synchronize_session=False)
        new_items = []
        for item in updated_items:
            item["order_id"] = order_id
            new_items.append(Item(**item))
        db.add_all(new_items)
        db.commit()

        return
    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")






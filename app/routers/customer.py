from collections import defaultdict
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from ..schemas.customer import CustomerReq, CustomerRespBasic, CustomerRespDetail
from ..models.customer import Customer
from ..models.order import Order
from ..models.item import Item
from sqlalchemy.orm import Session


router = APIRouter(prefix="/customers")

@router.get("/", status_code=200, response_model=List[CustomerRespBasic])
def get_customers(db: Session = Depends(get_db)):
    """ Get all customers """
    customers = db.query(Customer).all()
    return customers

@router.get("/{customer_id}", status_code=200, response_model=CustomerRespDetail)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """ Get one customer by id. """
    # select * from customers left join orders on orders.customer_id = customers.id left join items on orders.internal_id = items.order_id where customers.id = {customer_id}
    result = db.query(Customer, Order, Item).join(Order, Order.customer_id == Customer.id, isouter=True).join(Item, Item.order_id == Order.internal_id, isouter=True).filter(Customer.id == customer_id).all()
    if result:
        return parse_qry_result(result)
    raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

@router.post("/", status_code=201)
def create_customer(payload: CustomerReq, db: Session = Depends(get_db)):
    """ Create a new customer. If customer already exists (checked by email), it will raise exception """
    customer = db.query(Customer).filter(Customer.email == payload.email)
    if customer.first():
        raise HTTPException(status_code=400, detail=f"Customer with email {payload.email} already exists")
    new_customer = Customer(**payload.dict())    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def parse_qry_result(matrix) -> dict:
    """ Parse 2D matrix of result query, to proper JSON dict with nested lists of nested dict. """
    # easy case - customer has no orders
    print("in here")
    if not matrix[0].Order:
        ret_val = {}
        for attr in vars(matrix[0].Customer):
            if attr != "_sa_instance_state":
                ret_val[attr] = getattr(matrix[0].Customer, attr)
        ret_val["orders"] = None
        return ret_val

    # uneasy case: customer has 1-N orders each with 1-N items in it
    # parse items first
    N = len(matrix) - 1
    items = defaultdict(list)
    while N >= 0:
        order_id = 0 # this will be used to connect it
        item = {}
        for attr in vars(matrix[N].Item):
            if attr != "_sa_instance_state":
                attr_value = getattr(matrix[N].Item, attr)
                item[attr] = attr_value
                if attr == "order_id":
                    order_id = attr_value
        N -= 1
        items[order_id].append(item)

    # then orders - get rid of duplications first
    N = len(matrix) - 1
    unique_orders = set()
    while N >= 0:
        unique_orders.add(matrix[N].Order)
        N -= 1
    orders = []
    for o in unique_orders:
        order = {}
        for attr in vars(o):
            if attr != "_sa_instance_state":
                order[attr] = getattr(o, attr)
                if attr == "internal_id":
                    order["items"] = items.pop(getattr(o, attr)) # connect the porper items
        orders.append(order)
        N  -= 1

    # customer is just one and only 
    ret_val = {}
    for attr in vars(matrix[0].Customer):
        if attr != "_sa_instance_state":
            ret_val[attr] = getattr(matrix[0].Customer, attr)
    ret_val["orders"] = orders 
    print(ret_val)
    return ret_val

    

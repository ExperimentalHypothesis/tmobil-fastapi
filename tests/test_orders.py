from datetime import datetime
from app.schemas.order import OrderResp

# ------------- GET all orders

def test_get_orders(client, test_customer1, test_customer_order, test_customer_order2):
    res = client.get("/orders/")
    assert res.status_code == 200
    rjson = res.json()
    assert type(rjson) == list
    assert len(rjson) == 2

# ------------- GET one order by id

def test_get_order_404(client, test_customer1, test_customer_order):
    res = client.get("/orders/99")
    assert res.status_code == 404

def test_get_order(client, test_customer1, test_customer_order):
    res = client.get("/orders/1")
    assert res.status_code == 200
    rjson = res.json()
    assert "items" in rjson
    assert rjson["total_cost"] == 100
    assert rjson["customer_id"] == 1

# ------------- UPDATE order

def test_update_order(client, test_customer1, test_customer_order):
    data = {
        "total_cost": 200,
        "customer_id": 1,
        "items": [
            {
                "internal_id": 10,
                "price": 99,
                "description": "updated something",
                "order_id": 1
            }
        ]
    }
    res = client.put("/orders/1", json=data)
    assert res.status_code == 204
    updated = client.get("/orders/1")
    assert updated.status_code == 200
    rjson = updated.json()
    assert rjson["total_cost"] == 200
    assert rjson["items"][0]["description"] == "updated something"

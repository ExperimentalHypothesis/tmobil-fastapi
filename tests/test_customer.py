from datetime import datetime
from app.schemas.customer import CustomerRespDetail, CustomerRespBasic

# ------------ GET all customers

def test_get_customers(client, test_customer1, test_customer2):
    res = client.get("/customers/")
    assert res.status_code == 200
    rjson = res.json()
    assert type(rjson) == list
    assert len(rjson) == 2
    assert rjson[0]["email"] == "c1@gmail.com"

# ------------- GET customer by id
def test_get_customer_404(client, test_customer1):
    res = client.get("/customers/99")
    assert res.status_code == 404

def test_get_customer_without_orders(client, test_customer1):
    res = client.get("/customers/1")
    c = CustomerRespDetail(**res.json())
    assert c.email == "c1@gmail.com"
    assert c.phone == 111222333
    assert c.orders == None # this one has no orders
    assert res.status_code == 200

def test_get_customer_with_orders(client, test_customer1, test_customer_order):
    res = client.get("/customers/1")
    c = CustomerRespDetail(**res.json())
    assert c.email == "c1@gmail.com"
    assert c.phone == 111222333
    assert c.orders != None # now it has some orders
    assert res.status_code == 200

# --------------- POST customer

def test_create_customer_basic(client):
    resp = client.post("/customers/", json={"phone": 111222333, "email": "c1@gmail.com"})
    c = CustomerRespBasic(**resp.json())
    assert resp.status_code == 201
    assert c.email == "c1@gmail.com"
    assert c.phone == 111222333
    assert c.first_name == None
    assert c.ico == None

def test_create_customer_company(client):
    resp = client.post("/customers/", json={"phone": 111222333,"email": "c2@gmail.com", "ico": 111111111, "dic": "CZ111111111"})
    c = CustomerRespBasic(**resp.json())
    assert resp.status_code == 201
    assert c.email == "c2@gmail.com"
    assert c.phone == 111222333
    assert c.ico == 111111111
    assert c.dic == "CZ111111111"
    assert c.first_name == None

def test_customer_person(client):
    resp = client.post("/customers/", json={"phone": 111222333, "email": "c2@gmail.com", "first_name": "john", "last_name": "lennon", "dob": "1940-09-10"})
    c = CustomerRespBasic(**resp.json())
    assert resp.status_code == 201
    assert c.email == "c2@gmail.com"
    assert c.phone == 111222333
    assert c.ico == None
    assert c.dic == None
    assert c.first_name == "john"
    assert c.last_name == "lennon"
    assert c.dob == datetime(1940, 9, 10, 0, 0)

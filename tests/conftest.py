from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base, get_db
from app.main import app
from app.config import settings
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    """ Setup clean DB tables everytime """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    """ Setup test client with separated database for tests """
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db # swap the dev db for testing db
    yield TestClient(app)

@pytest.fixture
def test_customer1(client):
    data = {"phone": 111222333, "email": "c1@gmail.com"}
    res = client.post("/customers/", json=data)
    assert res.status_code == 201

@pytest.fixture
def test_customer2(client):
    data = {"phone": 111222333, "email": "c2@gmail.com"}
    res = client.post("/customers/", json=data)
    assert res.status_code == 201

@pytest.fixture
def test_customer_order(client):
    data = {
        "total_cost": 100,
        "customer_id": 1,
        "items": [
            {
                "internal_id": 10,
                "price": 10,
                "description": "something",
                "order_id": 1
            }
        ]
    }
    res = client.post("/orders/", json=data)
    assert res.status_code == 201


@pytest.fixture
def test_customer_order2(client):
    data = {
        "total_cost": 200,
        "customer_id": 1,
        "items": [
            {
                "internal_id": 20,
                "price": 20,
                "description": "something else",
                "order_id": 2
            }
        ]
    }
    res = client.post("/orders/", json=data)
    assert res.status_code == 201
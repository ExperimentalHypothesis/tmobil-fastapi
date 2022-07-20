from fastapi import FastAPI
from .database import engine
from .models import customer, order as models
from .routers import customer, order, item

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(order.router)
app.include_router(customer.router)
app.include_router(item.router)


@app.get("/")
def root():
    return {"msg": "working.."}









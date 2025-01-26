from fastapi import FastAPI
from pygments.lexers import data

from database import Database
from models import Register, AddProducts, DeleteProduct

db = Database("database.db")

app = FastAPI()

TOKEN = "0F8ofm1AYuuCiIU9uimnq4fnqsm7905zacLkeEmC2rDLgAYVYwsIE9fgAUPNaagQ"


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/products/add")
async def add_products(data: AddProducts):
    if data.token != TOKEN:
        return {"status": "BAD", "error": "Wrong Token"}
    for product in data.data:
        db.product_create(product.product_id, product.name, product.image, product.price)
    return {"status": "OK"}


@app.get("/products/all")
async def get_all_products():
    data = db.products_get_all()
    return {"data": data}


@app.post("/register")
async def register(data: Register):
    if data.token != TOKEN:
        return {"status": "BAD", "error": "Wrong Token"}
    db.user_create(
        user_id=data.user_id,
        username=data.username,
    )

    return {"status": "OK"}


@app.post("/products/delete")
async def delete_products(data: DeleteProduct):
    print(data)
    if data.token != TOKEN:
        return {"status": "BAD", "error": "Wrong Token"}
    db.product_delete(data.product_id)
    return {"status": "OK"}

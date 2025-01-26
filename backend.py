import json

from fastapi import FastAPI

from database import Database
from models import Register, AddProducts, DeleteProduct, GetUser, GetProduct, Order, HistoryGet

db = Database("database.db")

app = FastAPI()

TOKEN = "0F8ofm1AYuuCiIU9uimnq4fnqsm7905zacLkeEmC2rDLgAYVYwsIE9fgAUPNaagQ"


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/check_activation")
async def check_activation(data: GetUser):
    return db.user_get(data.user_id, "activated")


@app.get("/get_balance")
async def get_balance(data: GetUser):
    return db.user_get(data.user_id, "balance")


@app.get("/get_token")
async def get_token(data: GetUser):
    return db.user_get(data.user_id, "token")


@app.post("/create_user_if_not_exists")
async def create_user_if_not_exists(data: GetUser):
    if not db.check_user(data.user_id):
        db.user_create(data.user_id)
        return {"status": "OK"}
    return {"status": "BAD", "error": "user already exists"}


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
    if not db.check_user(data.user_id):
        return {"status": "BAD", "error": "user not exists"}
    db.user_set(data.user_id, "activated", 1)

    return {"status": "OK"}


@app.post("/products/delete")
async def delete_products(data: DeleteProduct):
    print(data)
    if data.token != TOKEN:
        return {"status": "BAD", "error": "Wrong Token"}
    db.product_delete(data.product_id)
    return {"status": "OK"}


@app.get("/products/get")
async def get_product(product: GetProduct):
    product_id, name, image, price = db.product_get_all(product.product_id)
    return {"product_id": product_id, "name": name, "image": image, "price": price}


@app.post("/order")
async def cmd_order(data: Order):
    if db.user_get(data.user_id, "token") != data.user_hash:
        return False
    balance = db.user_get(data.user_id, "balance")
    if balance < data.finish_money:
        return False
    balance -= data.finish_money
    db.user_set(data.user_id, "balance", balance)
    history = json.loads(db.user_get(data.user_id, "history"))
    history_ = history.get("history")
    history_.append(data.model_dump())
    history["history"] = history_
    db.user_set(data.user_id, "history", json.dumps(history))
    return True


@app.get("/history")
async def cmd_history(data: HistoryGet):
    if db.user_get(data.user_id, "token") != data.user_hash:
        return None
    return json.loads(db.user_get(data.user_id, "history"))

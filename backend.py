import json

from fastapi import FastAPI
import requests
from database import Database
from models import Register, AddProducts, DeleteProduct, GetUser, GetProduct, Order, HistoryGet, ChangePoints

from config import token as __TOKEN__

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

    URL = f"https://api.telegram.org/bot{__TOKEN__}/getChat"

    # Параметры запроса
    params = {
        "chat_id": data.user_id
    }

    # Отправка запроса
    response = requests.get(URL, params=params)
    username = None
    # Обработка результата
    if response.status_code == 200:
        _data = response.json()
        if _data.get("ok"):
            chat_info = _data.get("result", {})
            username = chat_info.get("username")
    print(db.get_all_admins())
    for us_id in db.get_all_admins():
        URL = f"https://api.telegram.org/bot{__TOKEN__}/sendMessage"
        text = f"Заказ от пользователя @{username}\n==========\n"
        for i in data.data.keys():
            product_id, name, image, price = db.product_get_all(int(i))
            numb = data.data[i]
            price *= numb
            text += f"{name} - {numb} шт. - {price}\n"
        text += f"==========\nКомментарий:\n{data.comment}"

        # Параметры запроса
        params = {
            "chat_id": us_id,
            "text": text
        }

        # Отправка запроса
        response = requests.post(URL, params=params)
        print(response.text, response.url)
    return True


@app.get("/history")
async def cmd_history(data: HistoryGet):
    if db.user_get(data.user_id, "token") != data.user_hash:
        return None
    return json.loads(db.user_get(data.user_id, "history"))


@app.get("/admins")
async def get_admins():
    return {"data": db.get_all_admins()}


@app.post("/change_points")
async def change_points(data: ChangePoints):
    balance = db.user_get(data.user_id, "balance")
    balance += data.points
    db.user_set(data.user_id, "balance", balance)
    return True


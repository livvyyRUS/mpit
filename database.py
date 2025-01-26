import sqlite3
from typing import Any

from models import Product
import secrets


class Database:
    def __init__(self, path_to_file: str):
        self._path_to_file = path_to_file
        self.db = sqlite3.connect(path_to_file)
        self.cursor = self.db.cursor()

    def user_create(
            self,
            user_id: int,
            balance: int = 0,
            role: str = "user",
            activated: int = 0,
            history: str = '{"history": []}',
            token: str = secrets.token_hex(32)
    ):
        self.cursor.execute(
            f'''INSERT INTO users (user_id, balance, role, activated, history, token) VALUES ({user_id}, {balance}, "{role}", {activated}, '{history}', "{token}")'''
        )
        self.db.commit()

    def user_set(
            self, user_id: int, item: str, data: Any
    ):
        print(data, type(data))
        data = f"""'{data}'""" if type(data) == str else data
        print(f'UPDATE users SET {item} = {data} WHERE user_id = {user_id}')
        self.cursor.execute(f'UPDATE users SET {item} = {data} WHERE user_id = {user_id}')
        self.db.commit()

    def user_get(self, user_id: int, item: str) -> Any:
        self.cursor.execute(f'SELECT {item} FROM users WHERE user_id = {user_id}')
        data = self.cursor.fetchone()
        return data[0]

    def product_create(
            self,
            product_id: int,
            name: str,
            image: str,
            price: float,
    ):
        self.cursor.execute(
            f"INSERT INTO products (product_id, name, image, price) VALUES ({product_id}, '{name}', '{image}', {price})")
        self.db.commit()

    def product_set(
            self, product_id: int, item: str, data: Any
    ):
        data = f'"{data}"' if type(data) == str else data
        self.cursor.execute(f'UPDATE products SET {item} = {data} WHERE product_id = {product_id}')
        self.db.commit()

    def products_get_all(self):
        self.cursor.execute('SELECT * FROM products')
        data = []
        for product in self.cursor.fetchall():
            product_id, name, image, price = product
            data.append(
                Product.model_validate({"product_id": product_id, "name": name, "image": image, "price": price}))
        return data

    def product_delete(self, product_id: int):
        self.cursor.execute(f'DELETE FROM products WHERE product_id = {product_id}')
        self.db.commit()

    def check_user(self, _user_id: int):
        self.cursor.execute('SELECT * FROM users')
        data = self.cursor.fetchall()
        for user in data:
            user_id, balance, role, activated, history, token = user
            if _user_id == user_id:
                return True
        return False

    def product_get_all(self, product_id: int):
        self.cursor.execute(f'SELECT * FROM products WHERE product_id = {product_id}')
        product_id, name, image, price = self.cursor.fetchone()
        return product_id, name, image, price


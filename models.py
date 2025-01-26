from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    name: str
    image: str
    price: int


class AddProducts(BaseModel):
    token: str
    data: list[Product]


class Register(BaseModel):
    token: str
    user_id: int


class DeleteProduct(BaseModel):
    token: str
    product_id: int


class Products(BaseModel):
    data: list[Product]


class GetProduct(BaseModel):
    product_id: int


class GetUser(BaseModel):
    user_id: int


class GetProduct(BaseModel):
    product_id: int

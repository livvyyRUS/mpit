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
    username: str


class DeleteProduct(BaseModel):
    token: str
    product_id: int

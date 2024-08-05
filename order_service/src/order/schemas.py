from pydantic import BaseModel


class Order(BaseModel):
    product_id: int
    price: float
    fee: float
    total: float
    quantity: int
    status: str


class OrderCreate(BaseModel):
    quantity: int
    product_id: int
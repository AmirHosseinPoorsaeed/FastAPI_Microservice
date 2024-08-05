from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import requests

from . import models, schemas
from ..rabbitmq_conf.producer import publish


def read_all(db: Session):
    db_orders = db.query(models.Order).all()
    return db_orders


def get(id: int, db: Session):
    db_order = db.query(models.Order).filter(
        models.Order.id == id).first()

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='order not found'
        )

    return db_order


def create(request: schemas.OrderCreate, db: Session):
    req = requests.get(f'http://localhost:8000/products/{request.product_id}')
    product = req.json()

    new_order = models.Order(
        **request.model_dump(),
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        status='pending'
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    publish(
        'order_created',
        {
            'product_id': new_order.product_id,
            'quantity': new_order.quantity
        }
    )

    return new_order

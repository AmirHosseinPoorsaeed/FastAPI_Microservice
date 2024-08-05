from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


def read_all(db: Session):
    db_products = db.query(models.Product).all()
    return db_products


def get(id: int, db: Session):
    db_product = db.query(models.Product).filter(
        models.Product.id == id).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )

    return db_product


def create(request: schemas.Product, db: Session):
    new_product = models.Product(**request.model_dump())
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def update(id: int, request: schemas.Product, db: Session):
    db_product = db.query(models.Product).filter(
        models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )
    
    db_product.name = request.name
    db_product.price = request.price
    db_product.quantity = request.quantity
    db.commit()

    return db_product


def delete(id: int, db: Session):
    db_product = db.query(models.Product).filter(
        models.Product.id == id)

    if not db_product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )

    db_product.delete(synchronize_session=False)
    db.commit()

    return f'product with id {id} deleted successfully'

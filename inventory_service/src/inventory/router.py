from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import schemas, repository as product
from .. import database


router = APIRouter(
    prefix='/products',
    tags=['Product']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.ProductShow])
def all(db: Session = Depends(get_db)):
    return product.read_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ProductShow)
def detail(id: int, db: Session = Depends(get_db)):
    return product.get(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ProductShow)
def create(request: schemas.Product, db: Session = Depends(get_db)):
    return product.create(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ProductShow)
def update(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    return product.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return product.delete(id, db)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import schemas, repository as order
from .. import database


router = APIRouter(
    prefix='/orders',
    tags=['Product']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return order.read_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.OrderCreate, db: Session = Depends(get_db)):
    return order.create(request, db)
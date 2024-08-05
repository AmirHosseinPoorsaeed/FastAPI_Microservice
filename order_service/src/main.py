from fastapi import FastAPI

from .order import models, router as order
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(order.router)

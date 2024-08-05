from fastapi import FastAPI

from .inventory import models, router as inventory
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(inventory.router)

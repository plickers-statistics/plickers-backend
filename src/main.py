
from fastapi import FastAPI

from src.lifespan import lifespan
from src.routers.api import api_router


app = FastAPI(lifespan = lifespan)
app.include_router(api_router)

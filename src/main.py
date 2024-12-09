
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.lifespan import lifespan
from src.routers.api import api_router


app = FastAPI(lifespan = lifespan)
app.include_router(api_router)
app.mount('/', StaticFiles(directory='public'), name='public')

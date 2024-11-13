
from fastapi import APIRouter

from src.routers.websocket import websocket_router


api_router = APIRouter(prefix = '/api')
api_router.include_router(websocket_router)

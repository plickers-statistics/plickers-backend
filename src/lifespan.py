
from contextlib import asynccontextmanager

from distributed_websocket import WebSocketManager
from fastapi import FastAPI

from src.database.DatabaseConnection import DatabaseConnection


database = DatabaseConnection(
	username  = 'root',
	password  = 'root',
	database  = '__plickers',
	charset   = 'utf-8',
	collation = 'utf8mb4_general_ci'
)

manager = WebSocketManager(
	broker_channel = 'channel:1',
	broker_url     = 'memory://'
)

@asynccontextmanager
async def lifespan (_: FastAPI):
	"""
	"""

	await manager.startup()
	yield
	await manager.shutdown()

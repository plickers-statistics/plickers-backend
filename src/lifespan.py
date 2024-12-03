
from contextlib import asynccontextmanager

from distributed_websocket import WebSocketManager
from fastapi import FastAPI

from src.database.DatabaseContext import DatabaseContext
from src.database.DatabaseRequests import DatabaseRequests


database_context = DatabaseContext(
	username  = 'root',
	password  = 'root',
	database  = '__plickers',
	charset   = 'utf-8',
	collation = 'utf8mb4_general_ci'
)

database_requests = DatabaseRequests(
	database = database_context
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


from contextlib import asynccontextmanager

from distributed_websocket import WebSocketManager
from fastapi import FastAPI

from src.database.DatabaseConnection import DatabaseConnection
from src.database.DatabaseRequests import DatabaseRequests


database_connection = DatabaseConnection(
	username  = 'root',
	password  = 'root',
	database  = '__plickers',
	charset   = 'utf-8',
	collation = 'utf8mb4_general_ci'
)

database_requests = DatabaseRequests(
	database = database_connection
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

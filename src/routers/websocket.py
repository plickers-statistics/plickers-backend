
from fastapi import APIRouter
from redis.commands.helpers import random_string
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.lifespan import manager, database
from src.lobby.Lobby import Lobby


websocket_router = APIRouter()

@websocket_router.websocket('/websocket')
async def websocket_endpoint (websocket: WebSocket) -> None:
	"""
	Новое вебсокет подключение
	"""

	identifier = random_string(length = 100)
	connection = await manager.new_connection(websocket, identifier)
	lobby      = Lobby(database, manager, connection)

	try:
		await lobby.handler()

	except Exception as error:
		await connection.send_json({
			'type' : 'error',
			'data' : str(error)
		})

	finally:
		manager.remove_connection(connection)

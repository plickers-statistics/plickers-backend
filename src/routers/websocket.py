
from datetime import datetime

from fastapi import APIRouter
from redis.commands.helpers import random_string
from starlette.websockets import WebSocket

from src.lifespan import manager, database_requests
from src.lobby.Lobby import Lobby


websocket_router = APIRouter()

@websocket_router.websocket('/websocket')
async def websocket_endpoint (websocket: WebSocket) -> None:
	"""
	Новое вебсокет подключение
	"""

	identifier = random_string(length = 100)
	connection = await manager.new_connection(websocket, identifier)
	lobby      = Lobby(database_requests, manager, connection)

	connected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	try:
		await lobby.handler()

	except Exception as error:
		await connection.send_json({
			'type' : 'error',
			'data' : 'type: ' + type(error).__name__ + ', text: ' + str(error)
		})

		raise error

	finally:
		manager.remove_connection(connection)

		disconnected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		database_requests.add_connection_to_history(
			connected_at    = connected_at,
			disconnected_at = disconnected_at,

			ip_address         = websocket.client.host,
			student_identifier = lobby.student_identifier,
			extension_version  = lobby.extension_version,
		)

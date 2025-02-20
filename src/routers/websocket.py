
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

	lobby.connected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	lobby.ip_address   = websocket.client.host

	try:
		await lobby.loop()

	except Exception as error:
		await connection.send_json({
			'type' : 'notification',
			'data' : '\n'.join([
				'[SERVER_ERROR]',
				'type: %s' % type(error).__name__,
				'text: %s' % str(error),
			])
		})

		raise error

	finally:
		manager.remove_connection(connection)

		disconnected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		database_requests.add_connection_to_history(
			connected_at    = lobby.connected_at,
			disconnected_at = disconnected_at,

			ip_address = lobby.ip_address,

			class_hash_code   = lobby.class_hash_code,
			student_hash_code = lobby.student_hash_code,
			extension_version = lobby.extension_version,
		)

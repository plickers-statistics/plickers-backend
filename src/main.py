
from contextlib import asynccontextmanager

from distributed_websocket import WebSocketManager, Message
from fastapi import FastAPI
from redis.commands.helpers import random_string
from starlette.websockets import WebSocketDisconnect, WebSocket

from src.Lobby import Lobby
from src.questions.Questions import Questions


@asynccontextmanager
async def lifespan (_: FastAPI):
	await manager.startup()
	yield
	await manager.shutdown()

app     = FastAPI(lifespan = lifespan)
manager = WebSocketManager('channel:1', broker_url = 'memory://')

@app.get('/api/questions')
async def get_questions ():
	return [question.__dict__ for question in Questions.collection.values()]

@app.websocket('/api/ws')
async def websocket_endpoint (ws: WebSocket) -> None:
	identifier = random_string(100)
	connection = await manager.new_connection(ws, identifier)
	lobby      = Lobby(connection, manager)

	try:
		await lobby.handler()
	except WebSocketDisconnect:
		manager.remove_connection(connection)


import json

from distributed_websocket import Connection, WebSocketManager, Message

from src.options.Option import Option
from src.questions.Question import Question
from src.questions.Questions import Questions


class Lobby:
	question : Question | None
	option   : Option   | None

	def __init__ (self, connection: Connection, manager: WebSocketManager):
		self.connection = connection
		self.manager    = manager

	async def handler (self):
		while True:
			message = await self.connection.receive_json()

			req_type = message['type']
			req_data = message['data']

			method_name = 'TYPE_' + req_type.replace('-', '_')
			method_link = getattr(self, method_name)

			await method_link(req_data)

	async def TYPE_check_update (self, req_data: str):
		if req_data != '0.0':
			await self.connection.send_json({
				"type": "new-update",
				"data": "0.0"
			})

	async def TYPE_new_question (self, req_data: dict[str]):
		self.question = Questions.get_or_create_question(req_data)
		self.question.participants += 1

	async def TYPE_answer_selected (self, req_data: dict[str]):
		if not hasattr(self, 'question'):
			raise ValueError('question not specified')

		if hasattr(self, 'option'):
			self.option.votes -= 1

		self.option = self.question.options[req_data['identifier']]
		self.option.votes += 1

		self.question.options.recalculate_percentages()

		self.manager.broadcast(Message(typ = '', data = {
			'type': 'options-recalculated',
			'data': {
				'formulationHTML' : self.question.formulationHTML,
				'identifier'      : self.question.identifier,
				'participants'    : self.question.participants,

				'options': [{
					'formulationHTML' : option.formulationHTML,
					'identifier'      : option.identifier,

					'percentage' : option.percentage,
					'votes'      : option.votes
				} for option in self.question.options.values()]
			}
		}))

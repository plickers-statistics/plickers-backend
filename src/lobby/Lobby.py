
from distributed_websocket import Connection, WebSocketManager, Message

from src.database.requests.DatabaseRequests import DatabaseRequests

from src.lobby.DTOs.NewQuizDTO import NewQuizDTO
from src.lobby.DTOs.validate_data import validate_data


class Lobby:
	"""
	Лобби подключения
	"""

	extension_version   : str | None = None
	student_identifier  : str | None = None
	question_identifier : int | None = None

	def __init__ (self, database: DatabaseRequests, manager: WebSocketManager, connection: Connection):
		self.database   = database
		self.manager    = manager
		self.connection = connection

	async def handler (self) -> None:
		"""
		Обрабатывает новые сообщения
		"""

		async for message in self.connection.iter_json():
			parameter_type = message['type']
			parameter_data = message['data']

			method_name = parameter_type + '_handler'
			method_link = getattr(self, method_name)

			await method_link(parameter_data)

	@validate_data
	async def new_quiz_handler (self, data: NewQuizDTO) -> None:
		"""
		Получена информация о пользователе
		"""

		assert self.student_identifier is None, 'You have already logged in before'

		self.extension_version  = data.version
		self.student_identifier = data.student.id

		if self.extension_version != '1.2':
			await self.connection.send_json({
				'type': 'notification',
				'data': 'Доступна новая версия => 1.2',
			})

		self.database.replace_or_add_class_room(
			identifier   = data.class_room.id,
			name         = data.class_room.name,
			teacher_name = data.class_room.teacher_name,
		)

		self.database.replace_or_add_student(
			identifier       = data.student.id,
			first_name       = data.student.first_name,
			class_identifier = data.class_room.id,
		)

	async def new_question_handler (self, data: dict[str, str | int | list]) -> None:
		"""
		Получена информация о вопросе
		"""

		assert self.student_identifier is not None, 'User information not transferred'

		# ===== ===== ===== ===== =====

		parameter_formulation_html = data['formulationHTML']
		parameter_identifier       = data['identifier']
		parameter_options          = data['choices']

		assert isinstance(parameter_formulation_html, str)
		assert isinstance(parameter_identifier,       int)
		assert isinstance(parameter_options,          list)

		# ===== ===== ===== ===== =====

		self.question_identifier = parameter_identifier

		# question
		self.database.add_question_if_not_duplicated(
			identifier       = parameter_identifier,
			formulation_html = parameter_formulation_html,
		)

		# options
		for option in parameter_options:
			option_formulation_html = option['formulationHTML']
			option_identifier       = option['identifier']

			assert isinstance(option_formulation_html, str)
			assert isinstance(option_identifier,       int)

			self.database.add_option_if_not_duplicated(
				question_identifier     = self.question_identifier,
				option_identifier       = option_identifier,
				option_formulation_html = option_formulation_html,
			)

		# answer
		self.database.add_answer_if_not_duplicated(
			student_identifier  = self.student_identifier,
			question_identifier = self.question_identifier,
		)

	async def new_answer_handler (self, data: int) -> None:
		"""
		Получена информация о выбранном ответе
		"""

		assert self.student_identifier is not None and self.question_identifier is not None, 'User or question information not passed'

		# ===== ===== ===== ===== =====

		assert isinstance(data, int)

		# ===== ===== ===== ===== =====

		self.database.change_user_answer(
			student_identifier  = self.student_identifier,
			question_identifier = self.question_identifier,
			option_identifier   = data,
		)

		# options recalculated
		options = self.database.get_answer_statistics(
			question_identifier = self.question_identifier,
		)

		self.manager.broadcast(Message(
			typ  = '',
			data = {
				'type': 'answers_recalculated',
				'data': options,
			}
		))

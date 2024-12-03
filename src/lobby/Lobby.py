
from distributed_websocket import Connection, WebSocketManager, Message

from src.database.requests.DatabaseRequests import DatabaseRequests


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

	async def new_quiz_handler (self, data: dict[str, str | dict[str, str]]) -> None:
		"""
		Получена информация о пользователе
		"""

		assert self.student_identifier is None, 'You have already logged in before'

		# ===== ===== ===== ===== =====

		parameter_version = data['version']

		parameter_class_room              = data['class_room']
		parameter_class_room_id           = parameter_class_room['id']
		parameter_class_room_name         = parameter_class_room['name']
		parameter_class_room_teacher_name = parameter_class_room['teacher_name']

		parameter_student            = data['student']
		parameter_student_id         = parameter_student['id']
		parameter_student_first_name = parameter_student['first_name']

		assert isinstance(parameter_version, str)

		assert isinstance(parameter_class_room_id,           str)
		assert isinstance(parameter_class_room_name,         str)
		assert isinstance(parameter_class_room_teacher_name, str)

		assert isinstance(parameter_student_id,         str)
		assert isinstance(parameter_student_first_name, str)

		# ===== ===== ===== ===== =====

		self.extension_version  = parameter_version
		self.student_identifier = parameter_student_id

		if self.extension_version != '1.2':
			await self.connection.send_json({
				'type': 'notification',
				'data': 'Доступна новая версия => 1.2',
			})

		self.database.replace_or_add_class_room(
			identifier   = parameter_class_room_id,
			name         = parameter_class_room_name,
			teacher_name = parameter_class_room_teacher_name,
		)

		self.database.replace_or_add_student(
			identifier       = parameter_student_id,
			first_name       = parameter_student_first_name,
			class_identifier = parameter_class_room_id,
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

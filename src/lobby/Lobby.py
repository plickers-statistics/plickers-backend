
from distributed_websocket import Connection, WebSocketManager, Message

from src.database.requests.DatabaseRequests import DatabaseRequests

from src.exceptions.CustomException import CustomException
from src.exceptions.ExtensionVersionException import check_extension_version

from src.DTOs.NewQuizDTO import NewQuizDTO
from src.DTOs.NewQuestionDTO import NewQuestionDTO
from src.DTOs.validate_data import validate_data


class Lobby:
	"""
	Лобби подключения
	"""

	ip_address   = ''
	connected_at = ''

	# ===== ===== ===== ===== =====

	extension_version : str | None = None

	class_hash_code   : str | None = None
	student_hash_code : str | None = None

	question_identifier : int | None = None

	def __init__ (self, database: DatabaseRequests, manager: WebSocketManager, connection: Connection):
		self.database   = database
		self.manager    = manager
		self.connection = connection

	async def loop (self) -> None:
		"""
		"""

		try:
			async for message in self.connection.iter_json():
				await self.handler(message)

		except CustomException as error:
			await self.connection.send_json({
				'type': 'notification',
				'data': '\n'.join([
					'[SERVER_ERROR]',
					'type: %s' % type(error).__name__,
					'text: %s' % str(error),
				])
			})

			await self.connection.close()

	async def handler (self, message: dict[str]) -> None:
		"""
		Обрабатывает новое сообщение
		"""

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

		assert self.student_hash_code is None, 'You have already logged in before'

		self.extension_version = data.version
		self.class_hash_code   = data.class_room.hash_code
		self.student_hash_code = data.student.hash_code

		self.connection.topics.add('class_room-' + self.class_hash_code)
		self.connection.topics.add('student-'    + self.student_hash_code)

		await check_extension_version(
			connection        = self.connection,
			extension_version = self.extension_version,
		)

		self.database.replace_or_add_class_room(
			hash_code    = data.class_room.hash_code,
			name         = data.class_room.name,
			teacher_name = data.class_room.teacher_name,
		)

		self.database.replace_or_add_student(
			hash_code       = data.student.hash_code,
			first_name      = data.student.first_name,
			class_hash_code = data.class_room.hash_code,
		)

	@validate_data
	async def new_question_handler (self, data: NewQuestionDTO) -> None:
		"""
		Получена информация о вопросе
		"""

		assert self.student_hash_code is not None, 'User information not transferred'

		# С помощью topics distributed_websocket определяет кому отправлять события
		self.connection.topics.discard('question-' + str(self.question_identifier))
		self.connection.topics.add    ('question-' + str(data.identifier))

		self.question_identifier = data.identifier

		# question
		self.database.add_question_if_not_duplicated(
			template = data.template,

			identifier       = data.identifier,
			formulation_html = data.formulation_html,
		)

		# options
		for option in data.options:
			self.database.add_option_if_not_duplicated(
				question_identifier     = self.question_identifier,
				option_identifier       = option.identifier,
				option_formulation_html = option.formulation_html,
			)

		# answer
		self.database.add_answer_if_not_duplicated(
			student_hash_code   = self.student_hash_code,
			question_identifier = self.question_identifier,
		)

	async def new_answer_handler (self, data: int) -> None:
		"""
		Получена информация о выбранном ответе
		"""

		assert self.student_hash_code is not None and self.question_identifier is not None, 'User or question information not passed'

		self.database.change_user_answer(
			student_hash_code   = self.student_hash_code,
			question_identifier = self.question_identifier,
			option_identifier   = data,
		)

		# options recalculated
		options = self.database.get_answer_statistics(
			question_identifier = self.question_identifier,
		)

		self.manager.send(Message(
			typ  = '',

			# Отправить всем, у кого такой же вопрос (идентификатор)
			topic = 'question-' + str(self.question_identifier),
			data  = {
				'type': 'answers_recalculated',
				'data': options,
			}
		))

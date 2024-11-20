
from distributed_websocket import Connection, WebSocketManager, Message

from src.database.DatabaseRequests import DatabaseRequests


class Lobby:
	"""
	Лобби подключения
	"""

	extension_version   : str | None = None
	user_identifier     : int | None = None
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

	async def new_connection_handler (self, data: dict[str, str | int]) -> None:
		"""
		Получена информация о пользователе
		"""

		assert self.user_identifier is None, 'You have already logged in before'

		# ===== ===== ===== ===== =====

		parameter_version    = data['version']
		parameter_identifier = data['identifier']
		parameter_name       = data['name']

		assert isinstance(parameter_version,    str)
		assert isinstance(parameter_identifier, int)
		assert isinstance(parameter_name,       str)

		# ===== ===== ===== ===== =====

		self.extension_version = parameter_version
		self.user_identifier   = parameter_identifier

		self.database.replace_if_exists_else_add_user(
			identifier = parameter_identifier,
			name       = parameter_name,
		)

	async def new_question_handler (self, data: dict[str, str | int | list]) -> None:
		"""
		Получена информация о вопросе
		"""

		assert self.user_identifier is not None, 'User information not transferred'

		# ===== ===== ===== ===== =====

		parameter_formulation_html = data['formulationHTML']
		parameter_identifier       = data['identifier']
		parameter_options          = data['options']

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
			user_identifier     = self.user_identifier,
			question_identifier = self.question_identifier
		)

	async def new_answer_handler (self, data: int) -> None:
		"""
		Получена информация о выбранном ответе
		"""

		assert self.user_identifier is not None and self.question_identifier is not None, 'User or question information not passed'

		assert data is not None

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute(
					'UPDATE `answers` SET `option_identifier` = %(option_identifier)s WHERE `user_identifier` = %(user_identifier)s AND `question_identifier` = %(question_identifier)s',
					{
						'user_identifier'     : self.user_identifier,
						'question_identifier' : self.question_identifier,
						'option_identifier'   : data
					}
				)

			# options recalculated
			with connection.cursor(dictionary = True) as cursor:
				cursor.execute('''
					SELECT
						`option_identifier`   AS `identifier`,
						COUNT(*)              AS `votes`,
						JSON_ARRAYAGG(`name`) AS `users`
					FROM `answers` JOIN `users` ON `answers`.`user_identifier` = `users`.`identifier`
					WHERE `question_identifier` = %(question_identifier)s
					GROUP BY `option_identifier` LIMIT 100
				''', {
					'question_identifier': self.question_identifier
				})

				options = cursor.fetchall()
				total   = sum([option['votes'] for option in options])

				for option in options:
					option['percentage'] = option['votes'] / total * 100

				self.manager.broadcast(Message(
					typ  = '',
					data = {
						'type': 'options_recalculated',
						'data': options
					}
				))

			connection.commit()

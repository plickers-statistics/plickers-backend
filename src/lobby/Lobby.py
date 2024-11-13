
from distributed_websocket import Connection, WebSocketManager
from mysql.connector.pooling import MySQLConnectionPool


class Lobby:
	"""
	Лобби подключения
	"""

	extension_version   : str | None = None
	user_identifier     : int | None = None
	question_identifier : int | None = None

	def __init__ (self, database: MySQLConnectionPool, manager: WebSocketManager, connection: Connection):
		self.database   = database
		self.manager    = manager
		self.connection = connection

	async def handler (self) -> None:
		"""
		Обрабатывает новые сообщения
		"""

		while True:
			message = await self.connection.receive_json()

			parameter_type = message['type']
			parameter_data = message['data']

			method_name = parameter_type + '_handler'
			method_link = getattr(self, method_name)

			await method_link(parameter_data)

	async def new_connection_handler (self, data: dict[str, str | int]) -> None:
		"""
		Получена информация о пользователе
		"""

		self.extension_version = data['version']
		self.user_identifier   = data['identifier']

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.callproc('REPLACE_IF_EXISTS_ELSE_ADD_USER', (
					data['identifier'],
					data['name']
				))

	async def new_question_handler (self, data: dict[str]) -> None:
		"""
		Получена информация о вопросе
		"""

		if self.user_identifier is None:
			raise ValueError('User information not transferred')

		self.question_identifier = data['identifier']

		with self.database.get_connection() as connection:

			# question
			with connection.cursor() as cursor:
				cursor.execute(
					'INSERT IGNORE INTO `questions` (`identifier`, `formulation_html`) VALUES (%(identifier)s, %(formulation_html)s)',
					{
						'identifier'       : data['identifier'],
						'formulation_html' : data['formulationHTML']
					}
				)

			# options
			for option in data['options']:
				with connection.cursor() as cursor:
					cursor.execute('''
						INSERT INTO `options`
							(`question_identifier`, `option_identifier`, `formulation_html`)
						SELECT %(question_identifier)s, %(option_identifier)s, %(formulation_html)s
						WHERE NOT EXISTS (
							SELECT 1 FROM `options` WHERE `question_identifier` = %(question_identifier)s AND `option_identifier` = %(option_identifier)s
						)
					''', {
						'question_identifier' : self.question_identifier,
						'option_identifier'   : option['identifier'],
						'formulation_html'    : option['formulationHTML']
					})

			# answer
			with connection.cursor() as cursor:
				cursor.execute('''
					INSERT INTO `answers`
						(`user_identifier`, `question_identifier`, `option_identifier`)
					SELECT %(user_identifier)s, %(question_identifier)s, NULL
					WHERE NOT EXISTS (
						SELECT 1 FROM `answers` WHERE `user_identifier` = %(user_identifier)s AND `question_identifier` = %(question_identifier)s
					)
				''', {
					'user_identifier'     : self.user_identifier,
					'question_identifier' : self.question_identifier
				})

			connection.commit()

	async def new_answer_handler (self, data: int) -> None:
		"""
		Получена информация о выбранном ответе
		"""

		if self.user_identifier is None or self.question_identifier is None:
			raise ValueError('User or question information not passed')

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

			connection.commit()

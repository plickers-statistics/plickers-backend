
from src.database.DatabaseConnection import DatabaseConnection


class DatabaseRequests:

	def __init__(self, database: DatabaseConnection):
		self.database = database

	def replace_if_exists_else_add_user (self, identifier: int, name: str) -> None:
		"""
		"""

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.callproc('REPLACE_IF_EXISTS_ELSE_ADD_USER', (identifier, name))

	def add_question_if_not_duplicated (self, identifier: int, formulation_html: str) -> None:
		"""
		"""

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute(
					'INSERT IGNORE INTO `questions` (`identifier`, `formulation_html`) VALUES (%(identifier)s, %(formulation_html)s)',
					{
						'identifier'       : identifier,
						'formulation_html' : formulation_html,
					}
				)

			connection.commit()

	def add_option_if_not_duplicated (self, question_identifier: int, option_identifier: int, option_formulation_html: str) -> None:
		"""
		"""

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute(
					'''
						INSERT INTO `options`
							(`question_identifier`, `option_identifier`, `formulation_html`)
						SELECT %(question_identifier)s, %(option_identifier)s, %(formulation_html)s
						WHERE NOT EXISTS (
							SELECT 1 FROM `options` WHERE `question_identifier` = %(question_identifier)s AND `option_identifier` = %(option_identifier)s
						)
					''',

					{
						'question_identifier' : question_identifier,
						'option_identifier'   : option_identifier,
						'formulation_html'    : option_formulation_html,
					}
				)

			connection.commit()

	def add_answer_if_not_duplicated (self, user_identifier: int, question_identifier: int) -> None:
		"""
		"""

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute(
					'''
						INSERT INTO `answers`
							(`user_identifier`, `question_identifier`, `option_identifier`)
						SELECT %(user_identifier)s, %(question_identifier)s, NULL
						WHERE NOT EXISTS (
							SELECT 1 FROM `answers` WHERE `user_identifier` = %(user_identifier)s AND `question_identifier` = %(question_identifier)s
						)
					''',

					{
						'user_identifier'     : user_identifier,
						'question_identifier' : question_identifier,
					}
				)

			connection.commit()

	def change_user_answer (self, user_identifier: int, question_identifier: int, option_identifier: int) -> None:
		"""
		"""

		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute(
					'UPDATE `answers` SET `option_identifier` = %(option_identifier)s WHERE `user_identifier` = %(user_identifier)s AND `question_identifier` = %(question_identifier)s',
					{
						'user_identifier'     : user_identifier,
						'question_identifier' : question_identifier,
						'option_identifier'   : option_identifier,
					}
				)

			connection.commit()

	def get_answer_statistics (self, question_identifier: int) -> list:
		"""
		"""

		with self.database.get_connection() as connection:
			with connection.cursor(dictionary=True) as cursor:
				cursor.execute(
					'''
						SELECT
							`option_identifier`   AS `identifier`,
							COUNT(*)              AS `votes`,
							JSON_ARRAYAGG(`name`) AS `users`
						FROM `answers` JOIN `users` ON `answers`.`user_identifier` = `users`.`identifier`
						WHERE `question_identifier` = %(question_identifier)s
						GROUP BY `option_identifier` LIMIT 100
					''',

					{
						'question_identifier': question_identifier,
					}
				)

				options = cursor.fetchall()
				total   = sum([option['votes'] for option in options])

				for option in options:
					option['percentage'] = option['votes'] / total * 100

				return options


from src.database.DatabaseContext import DatabaseContext


class DatabaseRequests:

	def __init__(self, database: DatabaseContext):
		self.database = database

	def replace_if_exists_else_add_class_room (
		self,

		identifier   : str,
		name         : str,
		teacher_name : str,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.callproc(
				'REPLACE_IF_EXISTS_ELSE_ADD_CLASS_ROOM',
				(identifier, name, teacher_name),
			)

	def replace_if_exists_else_add_student (
		self,

		identifier       : str,
		first_name       : str,
		class_identifier : str,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.callproc(
				'REPLACE_IF_EXISTS_ELSE_ADD_STUDENT',
				(identifier, first_name, class_identifier),
			)

	def add_question_if_not_duplicated (
		self,

		identifier       : int,
		formulation_html : str,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.execute(
				'INSERT IGNORE INTO `questions` (`identifier`, `formulation_html`) VALUES (%(identifier)s, %(formulation_html)s)',
				{
					'identifier'       : identifier,
					'formulation_html' : formulation_html,
				}
			)

	def add_option_if_not_duplicated (
		self,

		question_identifier     : int,
		option_identifier       : int,
		option_formulation_html : str,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
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

	def add_answer_if_not_duplicated (
		self,

		student_identifier  : str,
		question_identifier : int,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.execute(
				'''
					INSERT INTO `answers`
						(`student_identifier`, `question_identifier`, `option_identifier`)
					SELECT %(student_identifier)s, %(question_identifier)s, NULL
					WHERE NOT EXISTS (
						SELECT 1 FROM `answers` WHERE `student_identifier` = %(student_identifier)s AND `question_identifier` = %(question_identifier)s
					)
				''',

				{
					'student_identifier'  : student_identifier,
					'question_identifier' : question_identifier,
				}
			)

	def change_user_answer (
		self,

		student_identifier  : str,
		question_identifier : int,
		option_identifier   : int,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.execute(
				'UPDATE `answers` SET `changed_at` = CURRENT_TIMESTAMP(), `option_identifier` = %(option_identifier)s WHERE `student_identifier` = %(student_identifier)s AND `question_identifier` = %(question_identifier)s',
				{
					'student_identifier'  : student_identifier,
					'question_identifier' : question_identifier,
					'option_identifier'   : option_identifier,
				}
			)

	def get_answer_statistics (
		self,

		question_identifier : int,
	) -> list:
		"""
		"""

		with self.database.get_cursor(dictionary=True) as cursor:
			cursor.execute(
				'''
					SELECT
						`option_identifier`         AS `identifier`,
						COUNT(*)                    AS `votes`,
						JSON_ARRAYAGG(`first_name`) AS `users`
					FROM `answers` JOIN `students` ON `answers`.`student_identifier` = `students`.`identifier`
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

	def add_connection_to_history (
		self,

		connected_at    : str,
		disconnected_at : str,

		ip_address         : str,
		student_identifier : str | None,
		extension_version  : str | None,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.execute(
				'''
					INSERT INTO `connection_history`
						(`connected_at`, `disconnected_at`, `ip_address`, `student_identifier`, `extension_version`)
					VALUES
						(%(connected_at)s, %(disconnected_at)s, %(ip_address)s, %(student_identifier)s, %(extension_version)s);
				''',

				{
					'connected_at'    : connected_at,
					'disconnected_at' : disconnected_at,

					'ip_address'         : ip_address,
					'student_identifier' : student_identifier,
					'extension_version'  : extension_version,
				}
			)


from src.database.requests.RequestsAbstract import RequestsAbstract


class QuestionRequests(RequestsAbstract):

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
					INSERT INTO `question_options`
						(`question_identifier`, `option_identifier`, `formulation_html`)
					SELECT %(question_identifier)s, %(option_identifier)s, %(formulation_html)s
					WHERE NOT EXISTS (
						SELECT 1 FROM `question_options` WHERE `question_identifier` = %(question_identifier)s AND `option_identifier` = %(option_identifier)s
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
					INSERT INTO `student_answers`
						(`student_identifier`, `question_identifier`, `option_identifier`)
					SELECT %(student_identifier)s, %(question_identifier)s, NULL
					WHERE NOT EXISTS (
						SELECT 1 FROM `student_answers` WHERE `student_identifier` = %(student_identifier)s AND `question_identifier` = %(question_identifier)s
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
				'UPDATE `student_answers` SET `changed_at` = CURRENT_TIMESTAMP(), `option_identifier` = %(option_identifier)s WHERE `student_identifier` = %(student_identifier)s AND `question_identifier` = %(question_identifier)s',
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
					FROM `student_answers` JOIN `students_in_classes` ON `student_answers`.`student_identifier` = `students_in_classes`.`identifier`
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

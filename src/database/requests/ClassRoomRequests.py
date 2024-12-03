
from src.database.requests.RequestsAbstract import RequestsAbstract


class ClassRoomRequests(RequestsAbstract):

	def replace_or_add_class_room (
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

	def replace_or_add_student (
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

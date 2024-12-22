
from src.database.requests.RequestsAbstract import RequestsAbstract


class ClassRoomRequests(RequestsAbstract):

	def replace_or_add_class_room (
		self,

		hash_code    : str,
		name         : str,
		teacher_name : str,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.callproc(
				'REPLACE_IF_EXISTS_ELSE_ADD_CLASS_ROOM',
				(hash_code, name, teacher_name),
			)

	def replace_or_add_student (
		self,

		hash_code       : str,
		first_name      : str,
		class_hash_code : str,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.callproc(
				'REPLACE_IF_EXISTS_ELSE_ADD_STUDENT',
				(hash_code, first_name, class_hash_code),
			)


from src.database.DatabaseConnection import DatabaseConnection


class DatabaseRequests:

	def __init__(self, database: DatabaseConnection):
		self.database = database

	def replace_if_exists_else_add_user (self, identifier: int, name: str) -> None:
		with self.database.get_connection() as connection:
			with connection.cursor() as cursor:
				cursor.callproc('REPLACE_IF_EXISTS_ELSE_ADD_USER', (identifier, name))


from contextlib import contextmanager

from mysql.connector.abstracts import MySQLCursorAbstract

from src.database.DatabaseConnection import DatabaseConnection


class DatabaseContext(DatabaseConnection):
	"""
	"""

	@contextmanager
	def get_cursor (self, *args, **kwargs) -> MySQLCursorAbstract:
		"""
		Контекстный менеджер для работы с курсором
		"""

		connection = self.get_connection()

		try:
			with connection.cursor(*args, **kwargs) as cursor:
				yield cursor

		except Exception as error:
			connection.rollback()
			raise error

		finally:
			connection.close()

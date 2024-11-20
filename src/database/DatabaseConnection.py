
from typing import override

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection


class DatabaseConnection(MySQLConnectionPool):

	@override
	def get_connection(self) -> MySQLConnectionAbstract | PooledMySQLConnection:
		return super().get_connection()

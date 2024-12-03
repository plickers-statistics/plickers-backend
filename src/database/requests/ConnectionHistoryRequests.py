
from src.database.requests.RequestsAbstract import RequestsAbstract


class ConnectionHistoryRequests(RequestsAbstract):

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
					INSERT INTO `student_connection_history`
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

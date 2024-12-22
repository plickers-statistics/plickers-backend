
from src.database.requests.RequestsAbstract import RequestsAbstract


class ConnectionHistoryRequests(RequestsAbstract):

	def add_connection_to_history (
		self,

		connected_at    : str,
		disconnected_at : str,

		ip_address : str,

		class_hash_code   : str | None,
		student_hash_code : str | None,
		extension_version : str | None,
	) -> None:
		"""
		"""

		with self.database.get_cursor() as cursor:
			cursor.execute(
				'''
					INSERT INTO `student_connection_history`
						(`connected_at`, `disconnected_at`, `ip_address`, `class_hash_code`, `student_hash_code`, `extension_version`)
					VALUES
						(%(connected_at)s, %(disconnected_at)s, %(ip_address)s, %(class_hash_code)s, %(student_hash_code)s, %(extension_version)s);
				''',

				{
					'connected_at'    : connected_at,
					'disconnected_at' : disconnected_at,

					'ip_address' : ip_address,

					'class_hash_code'   : class_hash_code,
					'student_hash_code' : student_hash_code,
					'extension_version' : extension_version,
				}
			)


from src.database.DatabaseContext import DatabaseContext

from src.database.requests.ClassRoomRequests import ClassRoomRequests
from src.database.requests.QuestionRequests import QuestionRequests
from src.database.requests.ConnectionHistoryRequests import ConnectionHistoryRequests


class DatabaseRequests:

	def __init__(self, database: DatabaseContext):
		self.database = database

		# ===== ===== ===== ===== =====

		self._class_room_requests = ClassRoomRequests(database)

		self.replace_or_add_class_room = self._class_room_requests.replace_or_add_class_room
		self.replace_or_add_student    = self._class_room_requests.replace_or_add_student

		# ===== ===== ===== ===== =====

		self._question_requests = QuestionRequests(database)

		self.add_question_if_not_duplicated = self._question_requests.add_question_if_not_duplicated
		self.add_option_if_not_duplicated   = self._question_requests.add_option_if_not_duplicated
		self.add_answer_if_not_duplicated   = self._question_requests.add_answer_if_not_duplicated
		self.change_user_answer             = self._question_requests.change_user_answer
		self.get_answer_statistics          = self._question_requests.get_answer_statistics

		# ===== ===== ===== ===== =====

		self._connection_history_requests = ConnectionHistoryRequests(database)

		self.add_connection_to_history = self._connection_history_requests.add_connection_to_history

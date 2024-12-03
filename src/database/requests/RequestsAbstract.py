
from src.database.DatabaseContext import DatabaseContext


class RequestsAbstract:

	def __init__(self, database: DatabaseContext):
		self.database = database


class Option:
	"""
	Вариант ответа
	"""

	def __init__ (self, data: dict[str]):
		self.formulationHTML : str = data["formulationHTML"]
		self.identifier      : int = data["identifier"]

		self.percentage = 0
		self.votes      = 0

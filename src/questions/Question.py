
from src.options.Option import Option
from src.options.Options import Options


class Question:
	"""
	Вопрос
	"""

	def __init__ (self, data: dict[str]):
		self.formulationHTML : str = data["formulationHTML"]
		self.identifier      : int = data["identifier"]

		# ===== ===== ===== ===== =====

		self.options = Options()

		for choice in data["choices"]:
			option = Option(choice)
			self.options[option.identifier] = option

		# ===== ===== ===== ===== =====

		self.participants = 0

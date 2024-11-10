
from src.options.Option import Option


class Options (dict[int, Option]):
	"""
	Варианты ответов
	"""

	def recalculate_percentages (self):
		"""
		Пересчитать проценты ответов
		"""

		options = self.values()
		total   = sum([option.votes for option in options])

		for option in options:
			option.percentage = option.votes / total * 100


from src.questions.Question import Question


class Questions:
	'''
	'''

	collection: dict[int, Question] = {}

	@staticmethod
	def get_or_create_question (req_data: dict[str]) -> Question:
		'''
		'''

		identifier = req_data['identifier']

		if not identifier in Questions.collection:
			Questions.collection[identifier] = Question(req_data)

		return Questions.collection[identifier]

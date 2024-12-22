
from pydantic import BaseModel, Field


class QuestionOptionsDTO(BaseModel):
	"""
	"""

	formulation_html : str = Field(alias = 'formulationHTML')
	identifier       : int

class NewQuestionDTO(BaseModel):
	"""
	"""

	template : str

	formulation_html : str = Field(alias = 'formulationHTML')
	identifier       : int

	options : list[QuestionOptionsDTO]

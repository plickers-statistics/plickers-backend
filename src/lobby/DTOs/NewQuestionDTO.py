
from pydantic import BaseModel, Field


class QuestionOptionsDTO(BaseModel):
	"""
	"""

	formulation_html : str = Field(title = 'formulationHTML')
	identifier       : int

class NewQuestionDTO(BaseModel):
	"""
	"""

	formulation_html : str = Field(title = 'formulationHTML')
	identifier       : int
	options          : list[QuestionOptionsDTO]

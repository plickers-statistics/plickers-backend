
from pydantic import BaseModel, Field


class ClassRoomDTO(BaseModel):
	"""
	"""

	hash_code    : str = Field(alias = 'hashCode')
	name         : str
	teacher_name : str = Field(alias = 'teacherName')

class StudentDTO(BaseModel):
	"""
	"""

	hash_code  : str = Field(alias = 'hashCode')
	first_name : str = Field(alias = 'firstName')

class NewQuizDTO(BaseModel):
	"""
	"""

	class_room : ClassRoomDTO = Field(alias = 'classRoom')
	student    : StudentDTO
	version    : str

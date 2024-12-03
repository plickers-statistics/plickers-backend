
from pydantic import BaseModel


class ClassRoomDTO(BaseModel):
	"""
	"""

	id           : str
	name         : str
	teacher_name : str

class StudentDTO(BaseModel):
	"""
	"""

	id         : str
	first_name : str

class NewQuizDTO(BaseModel):
	"""
	"""

	class_room : ClassRoomDTO
	student    : StudentDTO
	version    : str

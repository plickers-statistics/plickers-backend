
from distributed_websocket import Connection

from src.exceptions.CustomException import CustomException


class ExtensionVersionException(CustomException):
	"""
	"""

async def check_extension_version (connection: Connection, extension_version: str) -> None:
	"""
	https://stackoverflow.com/questions/65718/what-do-the-numbers-in-a-version-typically-represent-i-e-v1-9-0-1
	"""

	values = extension_version.split('.', 2)

	major_version = int(values[0])
	minor_version = int(values[1])

	if major_version < 1 or minor_version < 3:
		raise ExtensionVersionException('Минимальная поддерживаемая версия => 1.3')

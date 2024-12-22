
from functools import wraps
from inspect import signature


def validate_data (method):
	"""
	"""

	@wraps(method)
	async def wrapper (self, data):
		"""
		"""

		information = signature(method)
		parameters  = information.parameters

		parameter_data_info = parameters['data']
		parameter_data_type = parameter_data_info.annotation

		return await method(
			self,
			parameter_data_type(**data)
		)

	return wrapper

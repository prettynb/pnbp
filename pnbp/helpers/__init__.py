import datetime

from .codeblock import CodeBlock
from .link import Link
from .tag import Tag
from .url import Url



""" 
""" 
def _convert_datetime(dt: str, as_mtime=False, as_date=False, as_time=False):
	""" mainly a helper function to convert from blog api,
		also accepts dt="now" -> "2021-07-13 12:30:22"

	:param dt: fastapi datetime object e.g. 
		'2021-05-13T11:22:10.373376' or
		'2019-12-15T15:32:34'

	:returns: 2021-07-13 12:30:22
	"""
	if as_mtime:
		return datetime.datetime.fromtimestamp(dt)

	if dt == 'now':
		if as_time:
			return datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
		elif as_date:
			return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

		return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

	try:
		return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f')
	except ValueError:
		try:
			return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
		except:
			raise Exception(f'Something went wrong with the format parsing of {dt}')











import inspect
from functools import wraps

from .models import Notebook



def pass_nb(func):
	""" custom non-click pass_param decorator,
		maily used to boilerplate each func rather than:
		```if not nb:
			nb = Notebook()```
		the point of which is to not be re-opening all .md
		unnecessarily when building commands that chain together.
		will handle regardless if nb passed via arg or kwarg
	"""
	@wraps(func)
	def inner(*args, **kwargs):
		
		if not 'nb' in inspect.signature(func).parameters.keys(): # why being wrapped?
			raise TypeError(f"@pass_nb decorator expecting keyword argument 'nb' in func '{func.__name__}' def parameters")

		args = list(args) # convert from tuple to manip

		nb = None # assume
		for i, a in enumerate(args):
			if isinstance(a, Notebook):
				nb = args.pop(i)

		if not 'nb' in kwargs.keys():
			kwargs.update({'nb': nb})

		if not isinstance(kwargs['nb'], Notebook):
			# print('fresh nb open by pass_ wrapping...')
			kwargs['nb'] = Notebook()

		if (note := kwargs.get('note')):
			# print('**', note)
			if isinstance(note, str):
				if (n := kwargs['nb'].get(note)):
					kwargs['note'] = n
				else:
					raise KeyError(f"note: '{note}' does not exist in the notebook!")

		if 'note' in kwargs.keys():
			if not (n := kwargs['note']):
				raise KeyError(f"note: '{n}' does not exist in the notebook!")

		return func(*args, **kwargs)

	return inner



def arrow_call(func):
	""" simple decorator printing "-> func" when func()
	"""
	@wraps(func)
	def inner(*args, **kwargs):
		print(f'-> {func.__name__}')
		return func(*args, **kwargs)
	return inner










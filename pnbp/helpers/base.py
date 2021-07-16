from collections import namedtuple
from functools import wraps



def prep_md_out(func):
	"""
	"""
	@wraps(func)
	def inner(*args, **kwargs):
		""" """
		note = kwargs.get('note')
		print(args, kwargs)

		if not note:
			for a in args:
				print('a: ', a)
				# if (note := isinstance(a, Note)):
				if str(a.__class__) == "<class 'pnbp.note.Note'>":
					note = a
					break

		if not note:
			raise ValueError("...")

		if not note.md_out:
			note.md_out = note.md

		return func(*args, **kwargs)

	return inner



class Helper:
	"""
	"""
	def __new__(cls, *args, **kwargs):
		""" """
		cls_name = cls.__name__
		attr_name = cls_name.lower()

		try:
			val = args[0]
		except IndexError:
			val = None

		_cls = namedtuple(cls_name, [attr_name])

		_cls.__str__ = cls.__str__
		_cls.__repr__ = cls.__repr__
		_cls.__eq__ = cls.__eq__

		for k,v in cls.__dict__.items():
			# print(k,v)
			if k != 'prep_md_out':
				setattr(_cls, k, v)
			# print(dir(_cls))

		if val:
			return _cls(val)

		return _cls

	def __repr__(self):
		""" """
		return f'{self.__class__.__name__}({self[0]})'

	def __str__(self):
		""" """
		return self[0]

	def __eq__(self, b):
		""" """
		if isinstance(b, str):
			if b == str(self):
				return True

			if self.__class__.__name__ == 'Tag':
				if b == self.tag.strip('#'):
					return True					
				return False

			

		return super().__eq__(b)

	@staticmethod
	def prep_md_out(func):
		"""
		"""
		@wraps(func)
		def inner(*args, **kwargs):
			""" """
			note = kwargs.get('note')
			print(args, kwargs)

			if not note:
				for a in args:
					print('a: ', a)
					# if (note := isinstance(a, Note)):
					if str(a.__class__) == "<class 'pnbp.note.Note'>":
						note = a
						break

			if not note:
				raise ValueError("...")

			if not note.md_out:
				note.md_out = note.md

			return func(*args, **kwargs)

		return inner





class Name(Helper):
	pass
	



















































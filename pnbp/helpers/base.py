from collections import namedtuple
from functools import wraps



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
		_cls.__add__ = cls.__add__

		for k,v in cls.__dict__.items():
			if k != 'prep_md_out':
				setattr(_cls, k, v)

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
					# may not be desired to match without (?), but
					return True					

			elif self.__class__.__name__ == 'Link':
				if b == self.note:
					# ...
					return True

			elif self.__class__.__name__ == 'Name':
				if b == self.asupper or b == self.astitle:
					return True

			return False

		return super().__eq__(b)

	def __add__(self, b):
		""" """
		if isinstance(b, str):
			return f'{str(self)}{b}'

		return super().__add__(self, b)

	@staticmethod
	def prep_md_out(mtd):
		""" a decorator 

			note: reference to "<class 'pnbp.note.Note'>":
				to allow an effective isinstance(a, pnbp.note.Note)
				without causing circular imports

		:param mtd: an @classmethod that does regex 
		"""
		@wraps(mtd)
		def inner(*args, **kwargs):
			""" """
			note = kwargs.get('note')
			print(args, kwargs)

			if not note:
				for a in args:
					print('a: ', a)
					# if isinstance(a, Note):
					if str(a.__class__) == "<class 'pnbp.note.Note'>":
						note = a
						break

			if not note:
				raise ValueError("...")

			if not note.md_out:
				note.md_out = note.md

			return mtd(*args, **kwargs)

		return inner



class Name(Helper):
	""" a Helper subclass is an for e.g. 

			Name = namedtuple("Name", "name")

			that 
				(a) defaults out to the string value of 
					the attribute (e.g. Name("dave") == "dave")
				(b) can define additional methods and properties
					associated with the subclass Name

			note: can't super() and assume
			you're getting the Helper's dunder mtds defined here.
			have access to all subclass mtds, but at __new__ (pre-instance)
			subclass *actually* subclasses namedtuple. e.g. on this subclass,
				
				def __eq__(self, b):
					# despite the fact that as Helper subclass
					# and my __eq__ mtd without on-class re-defining one
					# *is* Helper.__eq__, ...
					super().__eq__(b) # <- my direct parent is ultimately namedtuple, 
	"""
	@property
	def asupper(self):
		return self.name.upper()

	@property
	def astitle(self):
		return self.name.title()










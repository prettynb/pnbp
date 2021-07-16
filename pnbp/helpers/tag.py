import re
from collections import namedtuple

from .base import Helper #, prep_md_out



"""
"""
# class Tag(namedtuple('Tag', ['tag'])):
class Tag(Helper):
	""" 
	"""
	MDS_INT_TAG = r'([^\\)/>\'\w])#([A-Za-z]+)' 

	# def __repr__(self):
	# 	""" """
	# 	return f'Tag({self.tag})'

	# def __str__(self):
	# 	""" """
	# 	return self.tag
	# def __init__(self, *args, **kwargs):
	# 	super().__init__()

	# def __eq__(self, b):
	# 	""" """
	# 	# if isinstance(str, b)
	# 	# if not res and b == self.tag.strip('#'):
	# 	# 	# may not be desired to match without (?), but
	# 	# 	res = True
	# 	print('b', b, type(b))

	# 	return Helper.__eq__(self, b)

	# def __eq__(self, b):
	# 	""" """
	# 	if isinstance(b, str):
	# 		if b == str(self):
	# 			return True
	# 		elif b == self.tag.strip('#'):
	# 			# may not be desired to match without (?), but
	# 			return True

	# 	return super().__eq__(b)

	@staticmethod
	def regex_to_html(matchobj):
		""" regex #tags out to distinguish vs
			# space means md header1
			-> \\#tag
		"""
		return f"{matchobj.group(1)}\\#{matchobj.group(2)}"

	@classmethod
	@Helper.prep_md_out
	def replace_smdtags(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MDS_INT_TAG)		
		note.md_out = p.sub(Tag.regex_to_html, note.md_out)

		return note










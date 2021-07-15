import re
from collections import namedtuple



"""
"""
class Tag(namedtuple('Tag', ['tag'])):
	""" 
	"""
	MDS_INT_TAG = r'([^\\)/>\'\w])#([A-Za-z]+)' 

	def __repr__(self):
		""" """
		return f'Tag({self.tag})'

	def __str__(self):
		""" """
		return self.tag

	def __eq__(self, b):
		""" """
		if isinstance(b, str):
			if b == str(self):
				return True
			elif b == self.tag.strip('#'):
				# may not be desired to match without (?), but
				return True

		return super().__eq__(self, b)

	@staticmethod
	def regex_to_html(matchobj):
		""" regex #tags out to distinguish vs
			# space means md header1
			-> \\#tag
		"""
		return f"{matchobj.group(1)}\\#{matchobj.group(2)}"

	@classmethod
	def replace_smdtags(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MDS_INT_TAG)

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(Tag.regex_to_html, note.md_out)

		return note










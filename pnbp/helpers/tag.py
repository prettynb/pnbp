import re

from .base import Helper



"""
"""
class Tag(Helper):
	""" 
	"""
	MDS_INT_TAG = r'([^\\)/>\'\w])#([A-Za-z]+)' 

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










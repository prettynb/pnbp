import re
from collections import namedtuple

from .base import Helper #, prep_md_out



"""
"""
# class CodeBlock(namedtuple('CodeBlock', ['cblock'])):
class CodeBlock(Helper):
	"""
	"""
	MD_CODE = r'```([^`]*)```'
	MD_MERMAID = r'```mermaid([^`]*)```'
	
	@staticmethod
	def regex_mermaid_to_html(matchobj):
		""" required "scripts" in blog/static/layout.html 
		"""
		return f'<div class="mermaid">{matchobj.group(1)}</div>'

	@classmethod
	@Helper.prep_md_out
	def replace_mermaid(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MD_MERMAID)		
		note.md_out = p.sub(CodeBlock.regex_mermaid_to_html, note.md_out)

		return note

	@staticmethod
	def regex_unescape_comments(matchobj):
		""" where tags are escaped by int_tag_repl,
			regex \#comment -> #comment
			within html code blocks
		"""
		_code = matchobj.group(2).replace('\#', '#')

		return f'<code class="{matchobj.group(1)}">{_code}</code>'

	@classmethod
	@Helper.prep_md_out
	def fix_blocked_comments(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(r'<code class="(.+)">((.|\n)*)</code>')		
		note.md_out = p.sub(CodeBlock.regex_unescape_comments, note.md_out)

		return note











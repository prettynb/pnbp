import re

from .base import Helper



"""
"""
class CodeBlock(Helper):
	"""
	"""
	MD_CODE = r'```([^`]*)```'
	MD_MERMAID = r'```mermaid([^`]*)```'

	LANG_EXTS = {
		'py': 'py',
		'html': 'html',
		'mermaid': None,
		'bash': 'sh',
		'powershell': 'ps1',
		'txt': 'txt',
		'json': 'json'
		}
	
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

	@property
	def lang(self):
		""" ```lang \\n```

			the language string as used to 
			render the codeblock with syntax highlighting	
		"""
		_lang = self.codeblock.split()[0]

		if self.LANG_EXTS.get(_lang):
			return _lang

		return None

	@property
	def extn(self):
		""" ```python \\n``` => .py

			the language's file extension
		"""
		if self.lang:
			return self.LANG_EXTS[self.lang]

		return None

	@property
	def fname(self):
		""" a filename found in/if the
			top of a codeblock contains one:

				```py
				# hello.py
				print("hello world!")
				```
		"""
		clines = [x for x in self.codeblock.split() if x]
		_fname = ''
		if self.lang == 'py':
			if '#' == clines[1]:
				_fname = clines[2].strip()
			elif '#' in clines[1]:
				_fname = clines[1].strip().lstrip('#')

		if not re.match(rf'.+\.{self.extn}', _fname):
			_fname = ''

		return _fname








	














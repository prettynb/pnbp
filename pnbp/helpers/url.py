import re

from .base import Helper



"""
"""
class Url(Helper):
	"""
	"""
	MD_EXT_LINK = r'\[([^]]+)\]\(([^)]+)\)'
	HTTP_NAKED_LNK = r'([^\(])(https?://[^;,\s\]\*]+)'

	@classmethod
	def collect_urls(cls, note_md)->list:
		""" a regex search mtd 
			for http/https links
			available via each n.urls

		:param note_md: the .md content of an Note
		"""
		ext_links = []

		p = re.compile(cls.MD_EXT_LINK)
		for l in p.findall(note_md):
			ext_links.append(l[1])

		p = re.compile(cls.HTTP_NAKED_LNK)
		for l in p.findall(note_md):
			ext_links.append(l[1].rstrip('.').rstrip(')'))

		return ext_links

	@staticmethod
	def regex_nakedhref_to_md(matchobj):
		""" regex replacement function for e.g. http://www.blahblahblah.com -> 
			[http://www.blahblahblah.com](http://www.blahblahblah.com)
			markdown syntax so that on md -> html, these links are 
			then rendered clickable on md.markdown()
		"""
		return f"{matchobj.group(1)}[{matchobj.group(2)}]({matchobj.group(2)})"

	@classmethod
	@Helper.prep_md_out
	def replace_nakedhref(self, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(self.HTTP_NAKED_LNK)
		note.md_out = p.sub(Url.regex_nakedhref_to_md, note.md_out)

		return note

	@classmethod
	@Helper.prep_md_out
	def adjust_externallinks(cls, note):
		""" adding external link symbol, nofollow, and _blank target

		:param note: an Note instance
		"""
		_ext_icon = '<i class="bi bi-box-arrow-up-right" style="font-size:10px;"></i>'
		_add_attrs = 'rel="nofollow" target="_blank"'

		p = re.compile(r'<a href="(.*)">(.*)</a>') # taking advantage of our repl internal linked href='' vs ""
		extlnk_repl = lambda m: f'<a {_add_attrs} href="{m.group(1)}">{m.group(2)}</a> {_ext_icon}'

		note.md_out = p.sub(extlnk_repl, note.md_out)

		return note

	@property
	def baseurl(self):
		""" """
		_url = self.url.split('/')
		_url = [(i, p.replace('www.', '')) for i, p in enumerate(_url) if '.' in p]
		
		for x in ('.html', '.htm', '.php', '.asp'):
			for t in _url:
				if x in t[1]:
					_url.remove(t)

		if _url:
			if re.match(r'\w', _url[0][1][0]):
				return _url[0][1]

		return None

	@property
	def domain(self):
		""" """
		if self.baseurl:
			return ".".join(self.baseurl.split('.')[-2:])

		return None










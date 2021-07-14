import re
import datetime
from collections import namedtuple



""" 
""" 
def _convert_datetime(dt: str):
	""" mainly a helper function to convert from blog api,
		also accepts dt="now" -> "2021-07-13 12:30:22"

	:param dt: fastapi datetime object e.g. 
		'2021-05-13T11:22:10.373376' or
		'2019-12-15T15:32:34'

	:returns: 2021-07-13 12:30:22
	"""
	if dt == 'now':
		return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

	try:
		return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f')
	except ValueError:
		try:
			return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
		except:
			raise Exception(f'Something went wrong with the format parsing of {dt}')



""" 
"""
class Link(namedtuple('Link', ['link'])):
	"""
	"""
	MDS_INT_LNK = r'\[\[([^]]+)\]\]' 
	MDS_IMG_LNK = r'!\[\[([^]]+)\]\]'

	def __repr__(self):
		""" """
		return f'Link({self.link})'

	def __str__(self):
		""" """
		return self.link

	def __eq__(self, b):
		""" """
		if isinstance(b, str):
			if b == str(self):
				return True
			elif b == self.note:
				return True

		return super().__eq__(self, b)

	def __add__(self, b):
		""" """
		if isinstance(b, str):
			return f'{str(self)}{b}'

		return super().__add__(self, b)
	
	@staticmethod
	def regex_to_html(matchobj):
		""" regex replacement function for [[]] internal wiki links -> mysite.com/single-slug
		"""
		link = Link(matchobj.group(1))
		href = link.slugname
		val = link.link

		if link.subheader:

			if href.startswith('#'):
				if len([v for v in val.split('#') if v]) == 1:
					val = link.note + val

			val = val.replace("#", " > ")

		if link.label:
			val = link.label

		if not href.startswith('#'):
			href = f'/{href}'

		return f"<a href='{href}'>{val}</a>"

	@classmethod
	def replace_intlinks(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MDS_INT_LNK)

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(Link.regex_to_html, note.md_out)
		
		return note

	@staticmethod
	def regex_img_to_html(matchobj):
		""" regex replacement function for ![[]] internal image links -> mysite.com/single-slug
			todo: accept clean ( .png | .jpg ||)
		"""
		return f"""<img class="img-fluid" src='static/imgs/{matchobj.group(1)}'>"""

	@classmethod
	def replace_imglinks(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MDS_IMG_LNK)

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(Link.regex_img_to_html, note.md_out)

		return note

	@staticmethod
	def regex_append_subheader_attr_list(matchobj):
		""" """
		p = re.compile(r"(.+)<a href='/?.+'>(.+)</a>(.+)")
		repl = lambda m: f'{m.group(1)}{m.group(2)}{m.group(3)}'
		xreplmnt = p.sub(repl, matchobj.group(2))
		xreplmnt = p.sub(repl, xreplmnt)
		xreplmnt = p.sub(repl, xreplmnt)

		slugged = xreplmnt.strip().replace('_', '-').replace(' ', '-').lower()

		attr_list = '{: ' + f'id="{slugged}"' + ' }'

		return f'{matchobj.group(1)}{matchobj.group(2)} {attr_list}'

	@classmethod
	def add_header_ids(cls, note):
		""" providing access to sublink-ed via 
			[[mynote#section2]] to html 

		:param note: an Note instance
		"""
		p = re.compile(r'(#{1,6}\s)(.*)')

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(Link.regex_append_subheader_attr_list, note.md_out)

		return note

	@staticmethod
	def str_strip_name(matchobj):
		""" """
		return f'[[{matchobj.group(1).strip()}]]'

	@staticmethod
	def add_link_mention(matchobj):
		""" """
		return f'{matchobj.group(1)}[[{matchobj.group(2)}]]{matchobj.group(3)}'

	@staticmethod
	def remove_link_mention(matchobj):
		""" """
		return matchobj.group(2)

	@property
	def aslink(self):
		""" """
		return f'[[{self.link}]]'

	@property
	def asrawlink(self):
		""" """
		if self.subheader or self.label:
			return f'[[{self.note}]]'

		return self.aslink

	@property
	def label(self):
		""" """
		_label = None

		if '|' in self.link:
			try:
				note, _label = self.link.split('|')
				_label = _label.strip()

			except ValueError:
				# incorrect num vals to unpack
				# no label or [[a | broken | link]]
				pass

		return _label

	@property
	def subheader(self):
		""" """
		_subheader = None

		if '#' in self.link:
			try:
				note, _subheader = self.link.split('#')
				_subheader = _subheader.strip()

			except ValueError:
				# ... 
				pass

		return _subheader

	@property
	def note(self):
		""" 
		"""
		if self.subheader:
			return self.link.split('#')[0].strip()

		elif self.label:
			return self.link.split('|')[0].strip()

		return self.link

	@property
	def slugname(self):
		""" My Note Name -> my-note-name
		"""
		_name = self.link
		_sub = None

		if self.subheader or self.label:
			_name = self.note

			if self.subheader:
				_sub = '#' + self.subheader

		_name = re.sub(r'[^a-zA-Z1-9\s_-]+', '', _name)

		if _sub:
			_name = _name + _sub

		_name = _name.lower().replace(' ', '-').replace('_', '-')
		slugname = "-".join([w for w in _name.split('-') if w])

		if self.label:
			slugname = slugname.split('|')[0].rstrip('-')

		return slugname






class Tag(namedtuple('Tag', ['tag'])):
	""" 
	"""
	MDS_INT_TAG = r'([^\\)/>\'\w])#([A-Za-z]+)' 

	def __eq__(self, b):
		""" """
		if isinstance(b, str):
			if b == str(self):
				return True
			elif b == self.note:
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





class Url(namedtuple('Url', ['url', 'label'])):
	"""
	"""
	MD_EXT_LINK = r'\[([^]]+)\]\(([^)]+)\)'
	HTTP_NAKED_LNK = r'([^\(])(https?://[^;,\s\]\*]+)'

	def __new__(cls, url, label=None):
		""" """
		return super().__new__(cls, url, label)

	def __repr__(self):
		""" """
		return f'Url({self.url})'

	def __str__(self):
		""" """
		return self.url

	def __eq__(self, b):
		""" """
		if isinstance(b, str) == str(self):
			return True

		return super().__eq__(self, b)

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
	def replace_nakedhref(self, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(self.HTTP_NAKED_LNK)

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(Url.regex_nakedhref_to_md, note.md_out)

		return note

	@classmethod
	def adjust_externallinks(cls, note):
		""" adding external link symbol, nofollow, and _blank target

		:param note: an Note instance
		"""
		_ext_icon = '<i class="bi bi-box-arrow-up-right" style="font-size:10px;"></i>'
		_add_attrs = 'rel="nofollow" target="_blank"'

		p = re.compile(r'<a href="(.*)">(.*)</a>') # taking advantage of our repl internal linked href='' vs ""
		extlnk_repl = lambda m: f'<a {_add_attrs} href="{m.group(1)}">{m.group(2)}</a> {_ext_icon}'

		if not note.md_out:
			note.md_out = note.md
		
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





class CodeBlock(namedtuple('CodeBlock', ['cblock'])):
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
	def replace_mermaid(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MD_MERMAID)

		if not note.md_out:
			note.md_out = note.md
		
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
	def fix_blocked_comments(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(r'<code class="(.+)">((.|\n)*)</code>')

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(CodeBlock.regex_unescape_comments, note.md_out)

		return note

	









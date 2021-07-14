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

	@staticmethod
	def regex_nakedhref_to_md(matchobj):
		""" regex replacement function for e.g. http://www.blahblahblah.com -> 
			[http://www.blahblahblah.com](http://www.blahblahblah.com)
			markdown syntax so that on md -> html, these links are 
			then rendered clickable on md.markdown()
		"""
		return f"{matchobj.group(1)}[{matchobj.group(2)}]({matchobj.group(2)})"





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
				_label = label.strip()

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

	@staticmethod
	def regex_to_html(matchobj):
		""" regex replacement function for [[]] internal wiki links -> mysite.com/single-slug
		"""
		href = matchobj.group(1).strip().replace('_', '-').replace(' ', '-').lower()
		if not href.startswith('#'):
			href = f'/{href}'

		return f"<a href='{href}'>{matchobj.group(1)}</a>"

	@staticmethod
	def regex_img_to_html(matchobj):
		""" regex replacement function for ![[]] internal image links -> mysite.com/single-slug
			todo: accept clean ( .png | .jpg ||)
		"""
		return f"""<img class="img-fluid" src='static/imgs/{matchobj.group(1)}'>"""

	@staticmethod
	def regex_append_subheader_attr_list(matchobj):
		""" """
		slugged = matchobj.group(2).strip().replace('_', '-').replace(' ', '-').lower()
		attr_list = '{: ' + f'id="{slugged}"' + ' }'

		return f'{matchobj.group(1)}{matchobj.group(2)} {attr_list}'

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





class Tag(namedtuple('Tag', ['tag'])):
	""" """

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

	@staticmethod
	def regex_unescape_comments(matchobj):
		""" where tags are escaped by int_tag_repl,
			regex \#comment -> #comment
			within html code blocks
		"""
		_code = matchobj.group(2).replace('\#', '#')

		return f'<code class="{matchobj.group(1)}">{_code}</code>'

















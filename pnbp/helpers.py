import datetime
from collections import namedtuple


""" base md -> html 
	re.sub str replacement functions
"""
class Url(namedtuple('Url', ['url', 'label'])):

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
	




class Link(namedtuple('Link', ['link'])):

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


	# link
	@staticmethod
	def regex_to_html(matchobj):
		""" regex replacement function for [[]] internal wiki links -> mysite.com/single-slug
		"""
		href = matchobj.group(1).strip().replace('_', '-').replace(' ', '-').lower()
		if not href.startswith('#'):
			href = f'/{href}'

		return f"<a href='{href}'>{matchobj.group(1)}</a>"


# link img
def int_img_repl(matchobj):
	""" regex replacement function for ![[]] internal image links -> mysite.com/single-slug
		todo: accept clean ( .png | .jpg ||)
	"""
	return f"""<img class="img-fluid" src='static/imgs/{matchobj.group(1)}'>"""

# tag
def int_tag_repl(matchobj):
	""" regex #tags out to distinguish vs
		# space means md header1
		-> \\#tag
	"""
	return f"{matchobj.group(1)}\\#{matchobj.group(2)}"

# code
def md_mermaid_repl(matchobj):
	""" required "scripts" in blog/static/layout.html 
	"""
	return f'<div class="mermaid">{matchobj.group(1)}</div>'

# url
def md_nakedhref_repl(matchobj):
	""" regex replacement function for e.g. http://www.blahblahblah.com -> 
		[http://www.blahblahblah.com](http://www.blahblahblah.com)
		markdown syntax so that on md -> html, these links are 
		then rendered clickable on md.markdown()
	"""
	return f"{matchobj.group(1)}[{matchobj.group(2)}]({matchobj.group(2)})"

# tag (fixing...)
def comment_unescape(matchobj):
	""" where tags are escaped by int_tag_repl,
		regex \#comment -> #comment
		within html code blocks
	"""
	_code = matchobj.group(2).replace('\#', '#')

	return f'<code class="{matchobj.group(1)}">{_code}</code>'

# ...
def add_header_attr_list(matchobj):
	""" """
	slugged = matchobj.group(2).strip().replace('_', '-').replace(' ', '-').lower()
	attr_list = '{: ' + f'id="{slugged}"' + ' }'

	return f'{matchobj.group(1)}{matchobj.group(2)} {attr_list}'


""" cleanup re.sub str replacement functions
"""
# link
def str_strip_link(matchobj):
	""" """
	return f'[[{matchobj.group(1).strip()}]]'

def add_link_mention(matchobj):
	""" """
	return f'{matchobj.group(1)}[[{matchobj.group(2)}]]{matchobj.group(3)}'

def remove_link_mention(matchobj):
	""" """
	return matchobj.group(2)


""" tasks re.sub str replacement functions
"""
# task
def md_task_uncheck(matchobj):
	""" """
	t = matchobj.group(3).strip().replace(r'\t', ' ')

	if matchobj.group(1) == '\t':
		return f'\t- [ ] {t}'

	return f'- [ ] {t}'

# task 
def md_reoccurring_task_uncheck(matchobj):
	""" """
	return f'- [ ] {t}'



""" blog api connection helpers
""" 
def _convert_datetime(dt: str):
	""" 
	:param dt: fastapi datetime object e.g. 
		'2021-05-13T11:22:10.373376' or
		'2019-12-15T15:32:34'

	:returns: 2019-12-15 15:32:34
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






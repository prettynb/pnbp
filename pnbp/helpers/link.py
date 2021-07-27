import re
import platform

from .base import Helper



""" 
"""
class Link(Helper):
	"""
	"""
	MDS_INT_LNK = r'\[\[([^]]+)\]\]' 
	MDS_IMG_LNK = r'!\[\[([^]]+)\]\]'
	
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
	@Helper.prep_md_out
	def replace_intlinks(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MDS_INT_LNK)		
		note.md_out = p.sub(Link.regex_to_html, note.md_out)
		
		return note

	@staticmethod
	def regex_img_to_html(matchobj):
		""" regex replacement function for ![[]] internal image links -> mysite.com/single-slug
			todo: accept clean ( .png | .jpg ||)
		"""
		return f"""<img class="img-fluid" src='static/imgs/{matchobj.group(1)}'>"""

	@classmethod
	@Helper.prep_md_out
	def replace_imglinks(cls, note):
		""" a regex replace mtd 

		:param note: an Note instance
		"""
		p = re.compile(cls.MDS_IMG_LNK)
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
	@Helper.prep_md_out
	def add_header_ids(cls, note):
		""" providing access to sublink-ed via 
			[[mynote#section2]] to html 

		:param note: an Note instance
		"""
		p = re.compile(r'(#{1,6}\s)(.*)')		
		note.md_out = p.sub(Link.regex_append_subheader_attr_list, note.md_out)

		return note

	@staticmethod
	def str_strip_link(matchobj):
		""" """
		return f'[[{matchobj.group(1).strip()}]]'

	@staticmethod
	def str_expand_link(matchobj):
		""" """
		return f'[[ {matchobj.group(1).strip()} ]]'

	@staticmethod
	def add_link_mention(matchobj):
		""" """
		return f'{matchobj.group(1)}[[{matchobj.group(2)}]]{matchobj.group(3)}'

	@staticmethod
	def remove_link_mention(matchobj):
		""" """
		return matchobj.group(2)

	"""
	"""
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
	def subdirs(self):
		""" """
		if platform.system() == 'Windows':
			fpp = '\\'
		else:
			fpp = '/'

		if len((bydir := [x for x in self.link.split(fpp) if x])) > 1:
			subdirs = bydir[:-1]
			return subdirs

		return []

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

	def resolve(self, nb):
		""" 
		:param nb: an Notebook instance
		:returns: an Note instance
		"""
		return nb.get(self.note)












import os
import re
from collections import namedtuple, defaultdict

from .helpers import remove_link_mention



class Note(namedtuple('Note', ['name', 'md', 'links', 'tags', 'urls', 'cblocks', 'mtime'])):

	def __new__(cls, name, md, links, tags, urls, cblocks, mtime):
		"""
		:param str name: the filename stripped of .md
		:param str md: the in mem note context read from file
		:param list links: all regex found [[links]] 's in md
		:param list tags: all regex found #tag 's in md
		:param list urls: all regex found http/https links in md
		:param list cblocks: all regex found ```backtick code blocks```
		:param str mtime: the local md most recent modification date
			-> used against remote blog api to determine if POST required
		"""
		all_tags = [f'#{t}' for t in tags]

		_tags = list(set(all_tags.copy()))
		_remove = defaultdict(int)
		for t in _tags:
			for l in urls:
				if (num_occur := len(re.findall(t, l))):
					_remove[t] += num_occur
			for b in cblocks:
				if (num_occur := len(re.findall(t, b))):
					_remove[t] += num_occur

		for tag, occ in _remove.items():
			for x in range(occ):
				if tag in all_tags:
					all_tags.remove(tag)
		
		tags = list(set(all_tags)) # only legitimate #tag's remain
		urls = list(set(urls)) # <- doing here so that duplicate urls don't create tags
		links = list(set(links))

		return super().__new__(cls, name, md, links, tags, urls, cblocks, mtime)

	def __init__(self, *args, **kwargs):
		""" 
		:param md_out: safety first, make it hard to overwrite any note file
			-> set self.md_out = "as example, correct as is string instance"
			-> update file via self.save()
		"""
		self.md_out = '' 	

	def __str__(self):
		""" """
		return self.name

	@property
	def slugname(self):
		""" My Note Name -> my-note-name
		"""
		_name = re.sub(r'[^a-zA-Z1-9\s_-]+', '', self.name)
		_name = _name.lower().replace(' ', '-').replace('_', '-')
		slugname = "-".join([w for w in _name.split('-') if w])
		return slugname

	@property
	def sections(self)->list:
		"""	"""
		return [x.strip() for x in self.md.split('---')]

	@property
	def header(self):
		""" """
		if not re.match(r'^Links', self.sections[0]):
			return None

		return self.sections[0]

	def save(self, nb):
		""" save note to .md file on NOTE_PATH,
			if provided self.md_out has been updated.

		:param nb: the Notebook instance must be passed to save!
		"""
		if not isinstance(self.md_out, str):
			raise TypeError(f'{self.__class__.__name__}.md_out must be a str, not {type(self.md_out)}')

		if self.md_out:
			print(f'saving {self.name}...\n')
			# print(f'--->\n{self.md_out}')
			with open(os.path.join(nb.NOTE_PATH, self.name+'.md'), 'w') as nf:
				nf.write(self.md_out)

			return nb.open_note(self)

	def is_tagged(self, tag: str)->bool:
		""" check if note.md contains a #tag

		:param tag: the #tag in question
		"""
		tag = f"#{tag.lstrip('#')}" #failsafe

		if tag in self.tags:
			return True
			
		return False

	def is_linked(self, link: str="", at_all=False)->bool:
		""" check if note.md contains a [[link]]

		:param link: the [[link]] in question
		"""
		if at_all and self.links:
			return True

		if not link and not at_all:
			raise ValueError("Did you mean to call is_linked(at_all=True)?\nOtherwise, provide is_linked(link='internal-link-looking-for')")

		if link in self.links:
			return True

		return False

	def remove_links(self, links: list):
		""" if [[my link]] in links, -> if my link in links

		:param links: the [[link]] names to remove
		"""
		ns = self.md
		links = [l for l in links if not '.' in l] # keep images!
		
		for name in links:
			p = re.compile(fr'(\[\[\s?)({name})(\s?\]\])')

			if (ml := p.findall(ns)):
				for m in ml:
					print(f'[[{m[1]}]] --> ', m[1])

			ns = p.sub(remove_link_mention, ns)

		self.md_out = ns










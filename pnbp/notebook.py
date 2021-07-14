import os
import re
import json
import datetime
from collections import defaultdict
from getpass import getpass
# from pathlib import Path
import difflib

import markdown as md
import requests

from .note import Note
from .helpers import (Link, int_img_repl, int_tag_repl, # int_link_repl,
						md_mermaid_repl, md_nakedhref_repl, comment_unescape,
						_convert_datetime, add_header_attr_list)



class Notebook:
	""" class owned common regex patterns
	"""
	MDS_INT_LNK = r'\[\[([^]]+)\]\]' 
	MDS_IMG_LNK = r'!\[\[([^]]+)\]\]'
	MDS_INT_TAG = r'([^\\)/>\'\w])#([A-Za-z]+)' 

	MD_CODE = r'```([^`]*)```'
	MD_MERMAID = r'```mermaid([^`]*)```'

	MD_EXT_LINK = r'\[([^]]+)\]\(([^)]+)\)'
	HTTP_NAKED_LNK = r'([^\(])(https?://[^;,\s\]\*]+)'

	COMMIT_TAG = '#public'
	EXCLUDE_TAG = '#private'

	def __init__(self):

		self.NOTE_PATH = os.environ.get('NOTE_PATH')
		self.IMG_PATH = os.environ.get('IMG_PATH')
		self.HTML_PATH = os.environ.get('HTML_PATH')

		if not self.NOTE_PATH:
			raise ImportError("required to set NOTE_PATH environment variable to init a Notebook instance!")

		self.conf_file = os.path.join(self.NOTE_PATH, 'pnbp_conf.json')

		if not os.path.exists(self.conf_file):
			if not os.environ.get('NOTE_CONFIG') == 'off':
				print("an NOTE_PATH/pnbp-config.json file not found.")
				gen_empt = input("generate it from a template? (y/n): ")
				if gen_empt.lower() == 'y':

					empty_conf = {
							"IMG_PATH": "", "HTML_PATH": "", "VENV_PATH": "", 
							"API_BASE": "http://127.0.0.1:8000",
							"API_TOKEN": "", "PUB_LNK_ONLY": False,
							"NAV_BRAND": "", "NAV_PAGES": {},
							"FOOTER": "", "darkmode": False,
							"hljs_light": "default", "hljs_dark": "xt256",
							"merm_light": "default", "merm_dark": "dark",
							"COMMIT_TAG": '#public', "EXCLUDE_TAG": '#private',
							"HIDE_COMMIT_TAG": False, 
							}
					
					with open(self.conf_file, 'w') as cf:
						json.dump(empty_conf, cf, indent=4)

					print(f"generated (most empty/default) from template to\n{self.NOTE_PATH}/pnbp-config.json: \n{json.dumps(empty_conf, indent=4)}")
				else:
					print("NOTE_PATH/pnbp-config.json is only soft required, please see pnbp/settings_template.json for details.")
					print("Suppress warning+template offer message in the future by setting NOTE_CONFIG environment variable to 'off'.")
					self.conf_file = False
			else:
				self.conf_file = False

		if self.conf_file:
			with open(self.conf_file) as cf:
				self.config = json.load(cf)
		else:
			self.config = {} # lazy handle existance for conf_file=False

		if not self.IMG_PATH:
			# prefering set environment variable
			self.IMG_PATH = self.config.get('IMG_PATH')

		if not self.HTML_PATH:
			# but available to set in self.config 
			self.HTML_PATH = self.config.get('HTML_PATH')

		self.API_BASE = self.config.get('API_BASE')
		self.API_TOKEN = self.config.get('API_TOKEN')
		self.PUB_LNK_ONLY = self.config.get('PUB_LNK_ONLY')

		self.VENV_PATH = self.config.get('VENV_PATH') # see commands/subl.py

		if (tag := self.config.get("COMMIT_TAG")):
			# overwrite class default:
			self.COMMIT_TAG = tag

		if (tag := self.config.get("EXCLUDE_TAG")):
			# ... 
			self.EXCLUDE_TAG = tag

		self.notes = defaultdict()
		self.open_md()

	def __len__(self):
		""" the number of notes """
		return len(self.notes.keys())

	def open_note(self, f):
		""" 
		:param str f: the .md note to open
		"""
		if isinstance(f, Note):
			f = f.name + '.md'

		fname = f.split('.')[0]
		with open(os.path.join(self.NOTE_PATH, f), 'r') as fo:
			fo = fo.read()

			n = Note(
				name=fname,
				md=fo,
				links=[m.strip() for m in re.findall(self.MDS_INT_LNK, fo)],
				tags=[m[1] for m in re.findall(self.MDS_INT_TAG, fo)],
				urls=self.collect_urls(fo),
				cblocks=re.findall(self.MD_CODE, fo),
				mtime=datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(self.NOTE_PATH, f)))
				)

			self.notes.update({fname: n})

		return n

	def open_md(self)->dict:
		""" open all .md files from the self.NOTE_PATH path
			into memory as e.g. {"my note name": Note}
			-> available at nb.notes
		"""
		for f in os.listdir(self.NOTE_PATH):
			if f.endswith('.md'):
				self.open_note(f)

		self.notes = dict(sorted(self.notes.items()))

	def open(self):
		""" """
		self.open_md()

	def generate_note(self, name, md_out, overwrite=False):
		""" 
		:param name: the name of the note (without ".md") to generate
		:param md_out: the desired string to save to the notebook at "name.md"
		:param overwrite: 
		"""
		name = name.strip()

		if name in self.notes.keys() and not overwrite:
			raise FileExistsError(f"Cannot generate a new note with name {name}.")
 
		n = Note(name=name, md='', links=[], tags=[], urls=[], cblocks=[], mtime='')
		n.md_out = md_out
		n.save(self) # ^^ although instantiated empty, live access to attrs on nb instance

	def get(self, name)->Note:
		""" access the notes dict directly 

		:param name: name of the note
		:returns: Note instance or None
		"""
		if isinstance(name, Note):
			n = name
			return self.notes.get(n.name)

		name = name.replace('.md', '').replace('.html', '').replace('\\', '')

		if (note := self.notes.get(name)):
			return note

		for n in self.notes.values():
			if n.slugname == name:
				return n

		try: 
			name_in = name
			name = difflib.get_close_matches(name, [n for n in self.notes.keys()])[0]
			print(f"^^ {name} (by close match) ")
			return self.get(name)

		except IndexError:
			print(f"note: `{name_in}` does not exist in the notebook!")

		return None


	def get_tagged(self, tag)->list:
		""" 
		:param tag: the #tag in question
		:returns: a list of Note instances matching #tag
		"""
		t_notes = []
		for n in self.notes.values():
			if n.is_tagged(tag) and not n.name == 'all tags': # janky
				t_notes.append(n)

		return t_notes

	@property
	def tags(self)->list:
		""" a list of all found #tags in the Notebook instance
		"""
		ts = []
		for n in self.notes.values():
			for t in n.tags:
				ts.append(t)

		return sorted(list(set(ts)))

	@property
	def urls(self)->list:
		"""
		"""
		us = []
		for n in self.notes.values():
			for u in n.urls:
				us.append(u)

		return sorted(us)


	

	def find(self, regex):
		""" a user convenience method to effectively grep notebook
		"""
		print(f'regex: {regex}')

		notes = []
		for fn, n in self.notes.items():
			p = re.compile(regex)
			if (m := p.search(n.md)):
				print(f'\t -> {fn}')
				print(m)
				print(f'found: {m}')
				notes.append(n)

		return notes

	def find_and_replace(self, regex, replace):
		""" be careful, use find first
		"""
		if (ntc := self.find(regex)):
			for n in ntc:
				n.md_out = re.sub(regex, replace, n.md)
				n.save(self)

	def collect_urls(self, note)->list:
		""" a regex search mtd 
			for http/https links
			available via each n.urls

		:param note: the .md content of the Note
		"""
		ext_links = []

		p = re.compile(self.MD_EXT_LINK)
		for l in p.findall(note):
			ext_links.append(l[1])

		p = re.compile(self.HTTP_NAKED_LNK)
		for l in p.findall(note):
			ext_links.append(l[1].rstrip('.').rstrip(')'))

		return ext_links
	
	""" md->html str repl methods
		coupled with fxn from helpers.py
	"""
	def replace_imglinks(self, note):
		""" a regex replace mtd 

		:param note: the .md content of the Note
		"""
		p = re.compile(self.MDS_IMG_LNK)
		return p.sub(int_img_repl, note)

	def replace_intlinks(self, note):
		""" a regex replace mtd 

		:param note: the .md content of the Note
		"""
		p = re.compile(self.MDS_INT_LNK)
		return p.sub(Link.regex_to_html, note)

	def replace_smdtags(self, note):
		""" a regex replace mtd 

		:param note: the .md content of the Note
		"""
		p = re.compile(self.MDS_INT_TAG)
		return p.sub(int_tag_repl, note)

	def replace_mermaid(self, note):
		""" a regex replace mtd 

		:param note: the .md content of the Note
		"""
		p = re.compile(self.MD_MERMAID)
		return p.sub(md_mermaid_repl, note)

	def replace_nakedhref(self, note):
		""" a regex replace mtd 

		:param note: the .md content of the Note
		"""
		p = re.compile(self.HTTP_NAKED_LNK)
		return p.sub(md_nakedhref_repl, note)

	def fix_blocked_comments(self, note):
		""" a regex replace mtd 

		:param note: the .md content of the Note
		"""
		p = re.compile(r'<code class="(.+)">((.|\n)*)</code>')
		return p.sub(comment_unescape, note)

	def remove_nonpub_links(self, note):
		""" if #public note with [[not public]] links,
			remove them from html generation if nb.PUB_LNK_ONLY

		:param note: the .md content of the Note
		""" 
		remv = []
		for name in note.links:
			if (ln := self.get(name)):
				if not ln.is_tagged(self.COMMIT_TAG):
					remv.append(name)
			else:
				remv.append(name)

		note.remove_links(remv)

		return note.md_out

	def add_header_ids(self, note):
		""" providing access to sublink-ed via 
			[[mynote#section2]] to html 

		:param note: the .md content of the Note
		"""
		p = re.compile(r'(#{1,6}\s)(.*)')

		return p.sub(add_header_attr_list, note)

	def replace_strikethrough(self, note):
		""" ... 
		
		:param note: the .md content of the Note
		"""
		p = re.compile(r'(~~)(.*)(~~)')
		strike_repl = lambda m: f'<s>{m.group(2)}</s>'

		return p.sub(strike_repl, note)

	def replace_eqhighlight(self, note):
		""" ... 
		
		:param note: the .md content of the Note
		"""
		p = re.compile(r'(==)(.*)(==)')
		eqhl_repl = lambda m: f'<mark>{m.group(2)}</mark>'

		return p.sub(eqhl_repl, note)

	def adjust_externallinks(self, note):
		""" adding external link symbol, nofollow, and _blank target

		:param note: the .md content of the Note
		"""
		_ext_icon = '<i class="bi bi-box-arrow-up-right" style="font-size:10px;"></i>'
		_add_attrs = 'rel="nofollow" target="_blank"'

		p = re.compile(r'<a href="(.*)">(.*)</a>') # taking advantage of our repl internal linked href='' vs ""
		extlnk_repl = lambda m: f'<a {_add_attrs} href="{m.group(1)}">{m.group(2)}</a> {_ext_icon}'

		return p.sub(extlnk_repl, note)

	def hide_commit_tag(self, note):
		""" remove the #public tag from notes 
		"""
		return note.replace(self.COMMIT_TAG, '')


	def convert_to_html(self, note):
		""" apply all the regex method changes to 
			a single note

		:param note: the .md content of the Note
		"""
		if self.PUB_LNK_ONLY:
			note = self.remove_nonpub_links(note)
		else:
			note = note.md

		if self.config.get('HIDE_COMMIT_TAG') == True:
			note = self.hide_commit_tag(note)

		nout = self.replace_imglinks(note)
		nout = self.replace_intlinks(nout)
		nout = self.replace_smdtags(nout)
		nout = self.replace_mermaid(nout)
		nout = self.replace_nakedhref(nout)

		nout = self.add_header_ids(nout)

		nout = md.markdown(nout, extensions=['fenced_code',	'nl2br', 'markdown.extensions.tables', 'attr_list', 'footnotes'], use_pygments=True)

		nout = self.fix_blocked_comments(nout)
		nout = self.replace_strikethrough(nout)
		nout = self.replace_eqhighlight(nout)
		nout = self.adjust_externallinks(nout)

		return nout


	def write_commits_to_local_html(self):
		""" a local debugging mtd 
			-> self.HTML_PATH/.html ... 
		"""
		self.open_md() # fresh retrival 

		print(f'\nlocal commit: {self.HTML_PATH}')
		for n in self.notes.values():
			# if re.search(self.COMMIT_TAG, n.md):
			if n.is_tagged(self.COMMIT_TAG) and not n.is_tagged(self.EXCLUDE_TAG):
				nout = self.convert_to_html(note=n)
				of = open(os.path.join(self.HTML_PATH, f"{n.slugname}.html"), 'w')
				of.write(nout)
				of.close()

				print(f'\t{n.name} ---> {self.HTML_PATH}')

	""" pnbp-blog api connection methods:
	"""
	def get_headers(self):
		""" the request headers """
		return {'accept': 'application/json', 'authorization': f'Bearer {self.API_TOKEN}'}

	def refresh_token(self):
		""" request method to replace the authenticated user's bearer token 
		"""
		u = input('Username: ')
		p = getpass()
		h = self.get_headers()
		h.update({'Content-Type': 'application/x-www-form-urlencoded'})
		r = requests.post(f'{self.API_BASE}/api/token', data={'username': u, 'password': p}, headers=h)
		print(r)
		print(r.text)
		print(r.json())
		if r.status_code == 200:
			self.API_TOKEN = r.json()['access_token']

			with open(self.conf_file) as cf:
				config = json.load(cf)
				config.update({"API_TOKEN": self.API_TOKEN})

			with open(self.conf_file, 'w') as cf:
				json.dump(config, cf, indent=4)

	def get_authed_user(self):
		""" request method to get the authenticated user's username 
		"""
		h = self.get_headers()
		r = requests.get(f'{self.API_BASE}/api/users/me', headers=h)
		print(r)
		print(r.json())

	def get_api_home(self):
		""" request method to /api/ (testing auth) 
		"""
		h = self.get_headers()
		r = requests.get(f'{self.API_BASE}/api', headers=h)
		print(r.text)
		print(r.json())

	def get_pub_commits(self)->dict:
		""" (internal use)
			request method for a remote filepath check 
			for the purpose of making smarter POST updates
			against current publishments.
		"""
		h = self.get_headers()
		r = requests.get(f'{self.API_BASE}/api/publishments', headers=h)
		pub_data = r.json()

		nameMtime = {}
		for pub in pub_data:
			pub['mod_date'] = _convert_datetime(pub['mod_date'])
			nameMtime.update({pub['pub_name']: pub['mod_date']})

		return nameMtime

	def get_img_commits(self)->dict:
		""" (internal use)
			request method for a remote filepath check
			for the purpose of making smarter POST updates
			against current imgs.
		"""
		h = self.get_headers()
		r = requests.get(f'{self.API_BASE}/api/images', headers=h)
		img_data = r.json()

		nameMtime = {}
		for img in img_data:
			img['mod_date'] = _convert_datetime(img['mod_date'])
			nameMtime.update({img['img_name']: img['mod_date']})

		return nameMtime

	def delete_unlisted_post(self, rname):
		""" (internal use)
			request method to remove the HTML at filepath
			of Note(s) made non- #public
		"""
		h = self.get_headers()
		r = requests.delete(f'{self.API_BASE}/api/publishment/{rname}', headers=h)
		print(f'(removed) {r.json()["pub_name"]} -> {r}')


	def post_commits_to_blog_api(self, stage_only=False):
		""" the main POST method

		:param stage_only: if stage_only, print #public and don't commit
		"""
		self.open_md() # fresh retrival
		h = self.get_headers()

		pub_pub_data = self.get_pub_commits()
		pub_pub_names = pub_pub_data.keys()

		pub_img_data = self.get_img_commits()
		pub_img_names = pub_img_data.keys()

		print(f'\ncommits: (to {self.API_BASE})')
		post_names = []
		for n in self.notes.values():
			to_post = False
			fname = n.slugname + '.html'
			# if re.search(self.COMMIT_TAG, n.md):
			if n.is_tagged(self.COMMIT_TAG) and not n.is_tagged(self.EXCLUDE_TAG):
				post_names.append(fname)
				if fname in pub_pub_names:
					if pub_pub_data[fname] < n.mtime: # change has occured 
						to_post = True
				else: # it's newly #public
					to_post = True

			if to_post and not stage_only:
				nout = self.convert_to_html(note=n)
				r = requests.post(f'{self.API_BASE}/api/publishment',
					json={"name": n.slugname, "content": nout},
					headers=h
					)
				
				print(f'\t{n.name} -> {r}')

				for img in re.findall(self.MDS_IMG_LNK, n.md):
					if not img in pub_img_names:
						try:
							f = open(os.path.join(self.IMG_PATH, img), 'rb')
							r = requests.post(f'{self.API_BASE}/api/image',
								files={"filename": img, "file": f, "content_type": "image/jpeg"},
								headers=h
								)

							print(f'\t\t{img} -> {r}')
						except FileNotFoundError:
							print(f'\t\t{img} -> Broken image link!')
					else:
						print(f'\t\t{img} -> EXISTS!')

		if not stage_only:
			for p in pub_pub_names:
				if p not in post_names:
					self.delete_unlisted_post(p)
		else:
			print("\nnew pub: ")
			for p in [n for n in post_names if not n in pub_pub_names]:
				print(f'-> {p}')

			print("\nto remove:")
			for p in [n for n in pub_pub_names if not n in post_names]:
				print(f'-> {p}')

			print("\nall current pubs: ")
			for p in post_names:
				print(f'-> {p}')

			print("\n\n** stage_only=True, no changes made... ***")

	def blog_settings_post(self):
		""" request method to POST layout update 
			from self.NOTE_PATH/blog-settings.json 
			(see https://github.com/prettynb/pnbp-blog/blob/master/blog-settings.json
			for example)
		"""
		h = self.get_headers()

		_config = self.config.copy()

		bs_keys = tuple([
						"NAV_BRAND",
						"NAV_PAGES", 
						"FOOTER", 
						"darkmode", 
						"hljs_light", "hljs_dark", 
						"merm_light", "merm_dark"
						])

		for k in self.config.keys():
			if not k in bs_keys:
				del _config[k]

		r = requests.post(f'{self.API_BASE}/api/layout', json=_config, headers=h)
		print(r)

		# with open(os.path.join(self.NOTE_PATH, 'pnbp-blog-settings.json'), 'r') as f:
		# 	r = requests.post(f'{self.API_BASE}/api/layout', json=json.load(f), headers=h)
		# 	print(r)

	def create_api_user(self, username=''):
		""" request method to generate an pnbp-blog API user 
		"""
		if not username:
			username = input('username: ')

		password_1 = getpass()
		password_2 = getpass()
		if not password_1 == password_2:
			print('passwords do not match...')
			self.create_api_user(username)

		u = {
			"username": username,
			"password_hash": password_1
			}

		h = self.get_headers()
		r = requests.post(f'{self.API_BASE}/api/users', json=u, headers=h)
		print(r)
		print(r.json())
	
	def reset_api_password(self):
		""" request method to update the authed user's API password 
		"""
		p_1 = getpass()
		p_2 = getpass()		
		if not p_1 == p_1:
			print('passwords do not match...')
			self.reset_api_password()

		p = {"password_hash": p_1}
		h = self.get_headers()
		r = requests.post(f'{self.API_BASE}/api/users/me', json=p, headers=h)
		print(r)
		print(r.json())











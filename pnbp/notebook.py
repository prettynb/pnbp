import os
import re
import json
import getpass
import difflib
import random

import markdown as md
import requests

from .note import Note
from .helpers import Link, Tag, Url, CodeBlock, _convert_datetime



class Notebook:
	""" 
	"""
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
		
		if not os.environ.get('NOTE_NESTED') in ('flat', 'single', 'recurs', 'all'):
			self.config['NOTE_NESTED'] = 'flat'
		else:
			self.config['NOTE_NESTED'] = os.environ.get('NOTE_NESTED')

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
		else:
			self.COMMIT_TAG = '#public'

		if (tag := self.config.get("EXCLUDE_TAG")):
			# ... 
			self.EXCLUDE_TAG = tag
		else:
			self.EXCLUDE_TAG = '#private'

		self.notes = {}
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

		fname = f.split('.')[0].replace(self.NOTE_PATH, '')
		with open(os.path.join(self.NOTE_PATH, f), 'r') as fo:
			fo = fo.read()

			n = Note(
				name=fname,
				md=fo,
				links=[m.strip() for m in re.findall(Link.MDS_INT_LNK, fo)],
				tags=[m[1] for m in re.findall(Tag.MDS_INT_TAG, fo)],
				urls=Url.collect_urls(fo),
				codeblocks=re.findall(CodeBlock.MD_CODE, fo),
				mtime=_convert_datetime(os.path.getmtime(os.path.join(self.NOTE_PATH, f)), as_mtime=True),
				)

			self.notes.update({fname: n})

		return n

	def open_sub_md(self, subdir, search_hidden: bool)->list:
		""" helper method to walk through 
			self.NOTE_PATH subpaths (if necessary)

		:param subdir: a subdirectory
		:param search_hidden: whether or not to be walking .directories
		"""
		if subdir.startswith('.') and not search_hidden:
			return []

		if subdir in ('.git', '.obsidian', '__pycache__'):
			return []

		subpath = os.path.join(self.NOTE_PATH, subdir)
		
		for f in os.listdir(subpath):
			if f.endswith('.md'):
				self.open_note(os.path.join(subpath,f))

		subdirs = [d for d in os.listdir(subpath) if os.path.isdir(os.path.join(subpath, d))]
		subdirs = [d for d in subdirs if not d in ('.git', '.obsidian', '__pycache__')]

		if search_hidden:
			return subdirs
		else:
			return [d for d in subdirs if not d.startswith('.')]

	def open_sub_md_recurs(self, subdir, search_hidden: bool):
		""" ... 
		"""
		while (r := self.open_sub_md(subdir, search_hidden)):
			subdir = os.path.join(subdir, r.pop())
			self.open_sub_md_recurs(subdir, search_hidden)

	def open_md(self)->dict:
		""" open all .md files from the self.NOTE_PATH path
			into memory as e.g. {"my note name": Note}
			-> available at nb.notes
		"""
		NOTE_NESTED = self.config.get('NOTE_NESTED')
		srch_hidden = (True if NOTE_NESTED == 'all' else False)

		for f in os.listdir(self.NOTE_PATH):
			if f.endswith('.md'):
				self.open_note(f)
		
		if NOTE_NESTED != 'flat':
			for d in os.listdir(self.NOTE_PATH):
				if os.path.isdir(os.path.join(self.NOTE_PATH, d)):

					if NOTE_NESTED == 'single':
						self.open_sub_md(d, srch_hidden)
					
					elif NOTE_NESTED == 'recurs':
						self.open_sub_md_recurs(d, srch_hidden)
		
		self.notes = dict(sorted(self.notes.items()))

	def open(self):
		""" """
		self.open_md()

	def generate_note(self, name, md_out, overwrite=False, pnbp=False):
		""" 
		:param name: the name of the note (without ".md") to generate
		:param md_out: the desired string to save to the notebook at "name.md"
		:param overwrite: if overwrite=True, allow existing file to be re-written
		:param pnbp: if pnbp=True, tagging #pnbp to track and ignore
		"""
		name = name.strip()

		if name in self.notes.keys() and not overwrite:
			raise FileExistsError(f"Cannot generate a new note with name {name}.")
 
		n = Note(name=name, md='', links=[], tags=[], urls=[], codeblocks=[], mtime='')
		n.md_out = md_out

		if pnbp is True:
			n.md_out += '\n\n--- \n\n#pnbp'

		n.save(self) # ^^ although instantiated empty, live access to attrs on nb instance

	def get(self, name)->Note:
		""" access the notes dict directly 

		:param name: name of the note
		:returns: Note instance or None
		"""
		if isinstance(name, Note):
			n = name
			return self.notes.get(n.name)

		name = str(name)

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

	def get_random_note(self):
		"""
		:returns: a random note from the notebook
		"""
		return self.notes[random.choice([k for k in self.notes.keys()])]


	def get_tagged(self, tag)->list:
		""" 
		:param tag: the #tag in question
		:returns: a list of Note instances containing tag
		"""
		t_notes = []
		for n in self.notes.values():
			if n.is_tagged(tag):
				t_notes.append(n)

		return t_notes

	def get_linked(self, link)->list:
		"""
		:param link: the [[link]] in question
		:returns: a list of Note instances containing link
		"""
		l_notes = []
		for n in self.notes.values():
			if n.is_tagged(link):
				l_notes.append(n)

		return l_notes

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
	def links(self):
		""" a list of all .md Notes in the Notebook
		"""
		return sorted([fn for fn in self.notes.keys()])

	@property
	def urls(self)->list:
		""" a list of all Urls found in the Notebook
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

		print(f'{[n.name for n in notes]}')

		return notes

	def find_and_replace(self, regex, replace, notes=[]):
		""" 

		:param regex: 
		:param replace: 
		:param notes: 
		"""
		msg = "Notebook.find_and_replace requires a list of Notes to make replacements."
		if not notes:
			raise ValueError(f"{msg}\nnb.find_and_replace(regex='foo', replace='', notes=nb.find('foo'))")
		elif not isinstance(notes, list):
			raise ValueError(f"{msg}\nnb.find_and_replace(..., notes=[nb.get('bar'))]")
		else:
			# handle for string name -> note gets
			pass

		if (ntc := self.find(regex)):
			ntc = [n for n in ntc if n in notes]
			print('"replace" <- "regex" : n.name')
			for n in ntc:
				n.md_out = re.sub(fr'{regex}', replace, n.md)
				n.save(self)
				print(f'"{replace}" <- "{regex}" : {n.name}')

	""" preparing for api commits : 
	"""
	@classmethod
	def replace_strikethrough(cls, note):
		""" a regex replace mtd 
		
		:param note: an Note instance
		"""
		p = re.compile(r'(~~)(.*)(~~)')
		strike_repl = lambda m: f'<s>{m.group(2)}</s>'

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(strike_repl, note.md_out)

		return note

	@classmethod
	def replace_eqhighlight(cls, note):
		""" a regex replace mtd 
		
		:param note: an Note instance
		"""
		p = re.compile(r'(==)(.*)(==)')
		eqhl_repl = lambda m: f'<mark>{m.group(2)}</mark>'

		if not note.md_out:
			note.md_out = note.md
		
		note.md_out = p.sub(eqhl_repl, note.md_out)

		return note

	def remove_nonpub_links(self, note):
		""" if #public note with [[not public]] links,
			remove them from html generation if nb.PUB_LNK_ONLY

		:param note: an Note instance
		""" 
		remv = []
		for name in note.links:
			if (ln := self.get(name)):
				if not ln.is_tagged(self.COMMIT_TAG):
					remv.append(name)
			else:
				remv.append(name)

		note.remove_links(remv)
		# -> md_out is set initially here. 

		return note

	def hide_commit_tag(self, note):
		""" removes the #public tag (aka COMMIT_TAG) from
			the .md before export (if PUB_LNK_ONLY)

		:param note: an Note instance
		"""
		if not note.md_out:
			# -> if md_out is not set yet...
			note.md_out = note.md

		note.md_out.replace(self.COMMIT_TAG, '')

		return note

	def convert_to_html(self, note):
		""" apply all the regex method changes to 
			a single note

			md->html str repl methods
			coupled with mtds from helpers.py

		:param note: an Note instance
		::
		"""
		if self.PUB_LNK_ONLY:
			note = self.remove_nonpub_links(note)

		if self.config.get('HIDE_COMMIT_TAG') == True:
			note = self.hide_commit_tag(note)

		nout = Link.replace_imglinks(note)
		nout = Link.replace_intlinks(nout)
		nout = Tag.replace_smdtags(nout)
		nout = CodeBlock.replace_mermaid(nout)
		nout = Url.replace_nakedhref(nout)

		nout = Link.add_header_ids(nout)

		nout.md_out = md.markdown(nout.md_out, extensions=['fenced_code', 'nl2br', 'markdown.extensions.tables', 'attr_list', 'footnotes'], use_pygments=True)

		nout = CodeBlock.fix_blocked_comments(nout)
		nout = Notebook.replace_strikethrough(nout)
		nout = Notebook.replace_eqhighlight(nout)
		nout = Url.adjust_externallinks(nout)

		return nout

	def write_commits_to_local_html(self):
		""" a local debugging mtd 
			-> self.HTML_PATH/.html ... 
		"""
		self.open_md() # fresh retrival 

		print(f'\nlocal commit: {self.HTML_PATH}')
		for n in self.notes.values():

			if n.is_tagged(self.COMMIT_TAG) and not n.is_tagged(self.EXCLUDE_TAG):
				nout = self.convert_to_html(note=n)
				of = open(os.path.join(self.HTML_PATH, f"{n.slugname}.html"), 'w')
				of.write(nout.md_out)
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
		p = getpass.getpass()
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
					json={"name": n.slugname, "content": nout.md_out},
					headers=h
					)
				
				print(f'\t{n.name} -> {r}')

				for img in re.findall(Link.MDS_IMG_LNK, n.md):
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
						"NAV_BRAND", "NAV_PAGES", 
						"FOOTER", "TITLE",
						"darkmode", 
						"hljs_light", "hljs_dark", 
						"merm_light", "merm_dark"
						])

		for k in self.config.keys():
			if not k in bs_keys:
				del _config[k]

		r = requests.post(f'{self.API_BASE}/api/layout', json=_config, headers=h)

		print(r)

	def create_api_user(self, username=''):
		""" request method to generate an pnbp-blog API user 
		"""
		if not username:
			username = input('username: ')

		p_1 = getpass.getpass()
		p_2 = getpass.getpass()

		if not p_1 == p_2:
			print('passwords do not match...')
			self.create_api_user(username)

		u = {
			"username": username,
			"password_hash": p_1
			}

		h = self.get_headers()
		r = requests.post(f'{self.API_BASE}/api/users', json=u, headers=h)
		print(r)
		print(r.json())
	
	def reset_api_password(self):
		""" request method to update the authed user's API password 
		"""
		p_1 = getpass.getpass()
		p_2 = getpass.getpass()		

		if not p_1 == p_1:
			print('passwords do not match...')
			self.reset_api_password()

		p = {"password_hash": p_1}
		h = self.get_headers()
		r = requests.post(f'{self.API_BASE}/api/users/me', json=p, headers=h)
		print(r)
		print(r.json())











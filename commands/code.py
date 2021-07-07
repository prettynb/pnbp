import json
import os
from collections import defaultdict

import click

from pnbp.models import Notebook, Note
from pnbp.wrappers import pass_nb



LANG_EXTS = {
	'py': 'py',
	'html': 'html',
	'mermaid': None,
	'bash': 'sh',
	'powershell': 'ps1',
	'txt': 'txt',
	}



@pass_nb
def _collect_code_blocked(nb=None):
	""" if ```lang ``` -> nb/all code blocked.md 
	"""
	ns = "\n\n--- \n\n"
	for n in nb.notes.values():
		if n.cblocks:
			_c = n.cblocks.copy()

			for cb in _c:
				if not LANG_EXTS.get(cb.split()[0]):
					_c.remove(cb)
				if cb.startswith('mermaid'):
					_c.remove(cb)

			if _c:
				# if there's extension-ed code in the file:
				ns += f'[[{n.name}]]\n'

	nb.generate_note('all code blocked', ns, overwrite=True)


@pass_nb
@click.option('--lang', help=f"The code language to save. Any of these values: {json.dumps(LANG_EXTS, indent=4)}")
def _extract_code_blocks(lang: str, note: Note, nb=None):
	""" for each ````lang`` in note -> nb/code/n.name.ext
	"""
	if not lang in LANG_EXTS.keys() or not lang in LANG_EXTS.values():
		raise ValueError(f"--lang must be any of these values: {json.dumps(LANG_EXTS, indent=4)}")

	if lang in LANG_EXTS.keys():
		extn = LANG_EXTS[lang]
	else:
		extn = lang
		for k,v in LANG_EXTS.items():
			if v == extn:
				lang = k
				break

	cs = []
	for cb in n.cblocks:
		if cb.startswith(lang):
			cont = cb.lstrip(lang).lstrip('\n')
			cs.append(cont)

	if cs:
		if len(cs) == 1:
			cs = cs[0]
		else:
			cs = "\n\n".join(cs)

		cpth = os.path.join(nb.NOTE_PATH, 'code')

		if not os.path.exists(cpth):
			os.mkdir(cpth)

		if extn:
			with open(os.path.join(cpth, f'{n.name}.{extn}'), 'w') as f:
				f.write(cs)


@pass_nb
def _extract_all_codeblocks(note: Note, nb=None):
	""" for each valid LANG_EXTS found -> nb/code/n.name.ext
	"""
	n = note

	cs = defaultdict(list)

	for cb in n.cblocks:
		lang = cb.split()[0]
		extn = LANG_EXTS.get(lang)
		if extn:
			cont = cb.lstrip(lang).lstrip('\n')
			cs[extn].append(cont)

	cpth = os.path.join(nb.NOTE_PATH, 'code')

	if not os.path.exists(cpth):
		os.mkdir(cpth)

	for k,v in cs.items():
		if len(v) == 1:
			code = v[0]
		else:
			code = "\n\n".join(v)

		with open(os.path.join(cpth, f'{n.name}.{k}'), 'w') as f:
			f.write(code)










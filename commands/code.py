import json
import os
from collections import defaultdict

import click

from pnbp.models import Notebook, Note
from pnbp.wrappers import pass_nb
from pnbp.helpers import CodeBlock



@pass_nb
def _collect_code_blocked(nb=None):
	""" if ```lang ``` -> nb/all code blocked.md 
	"""
	ns = "\n\n--- \n\n"
	for n in nb.notes.values():
		if n.codeblocks:
			_collected = []
			for cb in n.codeblocks:
				if CodeBlock.LANG_EXTS.get(cb.codeblock.split()[0]):
					if not cb.codeblock.startswith('mermaid'):
						_collected.append(cb)

			if _collected:
				# if there's extension-ed code in the file:
				ns += f'[[{n.name}]]\n'

	nb.generate_note('all code blocked', ns, overwrite=True, pnbp=True)



@pass_nb
@click.option('-l', '--lang', help=f"The code language to save. Any of these values: {json.dumps(CodeBlock.LANG_EXTS, indent=4)}")
def _extract_code_blocks(lang: str, note: Note, nb=None):
	""" for each ````lang`` in note -> nb/code/n.name.ext
	"""
	cpth = os.path.join(nb.NOTE_PATH, 'code')

	if not os.path.exists(cpth):
		os.mkdir(cpth)

	if lang in CodeBlock.LANG_EXTS.keys():
		extn = CodeBlock.LANG_EXTS[lang]
	elif lang in CodeBlock.LANG_EXTS.values():
		extn = lang
		for k,v in CodeBlock.LANG_EXTS.items():
			if v == extn:
				lang = k
				break
	else:
		raise ValueError(f"--lang must be any of these values: {json.dumps(CodeBlock.LANG_EXTS, indent=4)}")

	n = note

	cs = []
	for cb in n.codeblocks:
		if cb.lang == lang:
			if cb.fname:
				with open(os.path.join(cpth, f'{cb.fname}'), 'w') as f:
					f.write(cb.codeblock.replace(cb.extn, '').lstrip('\n'))
			else:
				cont = cb.codeblock.lstrip(lang).lstrip('\n')
				cs.append(cont)
	if cs:
		if len(cs) == 1:
			# a single codeblock
			cs = cs[0]
		else:
			# combine multiple
			cs = "\n\n".join(cs)

		if extn:
			with open(os.path.join(cpth, f'{n.name}.{extn}'), 'w') as f:
				if extn == 'json':
					json.dump(cs, f, indent=4)
				else:
					f.write(cs)



@pass_nb
def _extract_all_code_blocks(note: Note, nb=None):
	""" for each valid LANG_EXTS found -> nb/code/n.name.ext
	"""
	cpth = os.path.join(nb.NOTE_PATH, 'code')

	if not os.path.exists(cpth):
		os.mkdir(cpth)

	n = note

	cs = defaultdict(list)

	for cb in n.codeblocks:

		if cb.extn:
			if cb.fname:
				with open(os.path.join(cpth, f'{cb.fname}'), 'w') as f:
					f.write(cb.codeblock.replace(cb.extn, '').lstrip('\n'))
			else:
				cont = cb.codeblock.lstrip(cb.lang).lstrip('\n')
				cs[cb.extn].append(cont)

	for k,v in cs.items():
		# by language ...
		if len(v) == 1:
			# a single codeblock
			code = v[0]
		else:
			# combine them
			code = "\n\n".join(v)

		with open(os.path.join(cpth, f'{n.name}.{k}'), 'w') as f:
			if k == 'json':
				json.dump(code, f, indent=4)
			else:
				f.write(code)










import os
import re
import inspect
import subprocess

from pnbp.wrappers import pass_nb

"""
NOTE: all imported to and locally defined collect.py
"_collect" fxns are called in _nb_collect_all (nb-collect-all)
and made avail individually (e.g. collect-tasks-note) automatically
"""
from .code import _collect_code_blocked
from .tasks import _collect_tasks_note
from .graph import _collect_public_graph, _collect_all_graphs
from .subl import _collect_subl_projs
from .commit import _collect_git_diff


""" commands writing collections to specific notebook files:
"""
@pass_nb
def _collect_all_stats(nb=None):
	""" ... stats (incl [[links]] to nb-collect-all "all *" entries)
	"""
	pnbp_generated = [n.linkname for n in nb.notes.values() if n.is_tagged("#pnbp")]

	num_notes = len(nb) - len(pnbp_generated)
	cont = f'\nnum_notes = {num_notes}'

	num_chars = sum([len(n.md) for n in nb.notes.values() if not n.is_tagged("#pnbp")])
	cont += f'\nnum_chars = {num_chars}'

	cont += f'\n\n--- \n\nall pnbp generated notes:\n'
	cont += "\n".join(pnbp_generated)

	nb.generate_note('all stats', cont, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_notes(nb=None):
	""" all .md files linked -> nb/all notes.md
	"""
	ns = sorted(list(nb.notes.values()), key=lambda n: n.mtime, reverse=True)

	nb.generate_note(
		'all notes',
		"".join([f"[[{n.name}]] {n.mtime}\n" for n in ns]),
		overwrite=True,
		pnbp=True
		)


@pass_nb
def _collect_all_urls(nb=None):
	""" all regex-ed http-based urls -> nb/all urls.md
	"""
	all_urls = []
	for n in nb.notes.values():
		if n.name not in ('all urls'):
			for u in n.urls:
				all_urls.append(u)

	nb.generate_note(
		'all urls', 
		'\n'.join(str(l) for l in all_urls), 
		overwrite=True,
		pnbp=True
		)


@pass_nb
def _collect_all_public(nb=None):
	""" if note contains #public -> notebook/all public.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if n.is_tagged(nb.COMMIT_TAG)])
	ns = "\n#public posts:\n\n --- \n\n" + ns

	nb.generate_note('all public', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_terms(nb=None):
	""" if found [[TERMS]] -> nb/TERMS.md
	"""
	TERMS_NOTE = nb.config.get('TERMS_NOTE')

	if not TERMS_NOTE:
		TERMS_NOTE = 'TERMS'

	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if n.is_linked(TERMS_NOTE)])
	ns = f"\nall [[{TERMS_NOTE}]] :\n\n --- \n\n" + ns

	nb.generate_note(TERMS_NOTE, ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_unlinked(nb=None):
	""" if not a single [[]] found 
		-> nb/all unlinked.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if not n.links])
	ns = "\nall unlinked :\n\n --- \n\n" + ns

	nb.generate_note('all unlinked', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_empty(nb=None):
	""" if a note is created on path w/out context 
		-> nb/all empty.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if len(n.md) < 4])
	ns = "\nall empty :\n\n --- \n\n" + ns

	nb.generate_note('all empty', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_unheadered(nb=None):
	""" if not "Links: ..." at the first line, 
		-> nb/all unheadered.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if not n.header])
	ns = "\nall unheadered :\n\n --- \n\n" + ns

	nb.generate_note('all unheadered', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_moc(nb=None):
	""" "maps of content" via capitalization (e.g. [[PYTHON]]) 
		-> nb/all MOC.md
	"""
	MOC_TAG = nb.config.get('MOC_TAG')
	CONT_TAG = nb.config.get('CONT_TAG')

	if not MOC_TAG:
		MOC_TAG = '#moc'
	if not CONT_TAG:
		CONT_TAG = '#cont'

	ns = [n for n in nb.notes.values() if not n.is_tagged(CONT_TAG)]
	ns = [n for n in ns if n.is_tagged(MOC_TAG) or n.name.isupper()]
	ns = "".join([f"[[{n.name}]]\n" for n in ns])
	ns = "\nall MOC :\n\n --- \n\n" + ns

	nb.generate_note('all MOC', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_tags(nb=None):
	""" a fancy generated note showing #tag per [[]] (and [[]] per #tag)
		-> nb/all tags.md
	"""
	ns = []
	
	ns.append(', '.join([t.tag for t in nb.tags]))
	
	ns.append('\n--- ')

	for t in nb.tags:
		t_w = f'{t} - '
		for n in nb.get_tagged(t):
			if not n.name == 'all tags':
				t_w += f' [[{n.name}]], '

		ns.append(t_w.rstrip(', '))

	ns.append('\n--- ')

	for n in nb.notes.values():
		if not n.name == 'all tags':
			fn_w = f'[[{n.name}]] - '

			if n.tags:
				for t in n.tags:
					fn_w += f' #{t}, '

				ns.append(fn_w.rstrip(', '))
	
	nb.generate_note(
		'all tags', 
		'\n'.join(str(ft) for ft in ns),
		overwrite=True,
		pnbp=True
		)


@pass_nb
def _collect_nonexistant_links(nb=None):
	""" ... -> nb/all nonexistant links.mb
	"""
	ns = "\n\n---\n\n"

	for n in nb.notes.values():
		_oldl = []
		for name in n.links:
			if not nb.get(name):
				print(f'\[\[{name}\]\]')
				_oldl.append(f'\[\[{name}\]\]')

		if _oldl:
			print(f'\n[[{n.name}]] :\n --> ')
			ns += f'\n[[{n.name}]] :\n --> '
			for ol in _oldl:
				ns += f'{ol}, '
			ns += '\n'

	nb.generate_note('all nonexistant links', ns, overwrite=True, pnbp=True)




""" !!! NOTE: all imported _collect* calls here: 
"""
@pass_nb
def _nb_collect_all(nb=None):
	""" perform all collect- commands in succession
	"""
	for k, func in globals().items():
		if k.startswith('_collect') and inspect.isfunction(func):
			print(f'{func.__name__} -->')
			func(nb) #call each function with the nb instance passed 










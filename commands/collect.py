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
from .cleanup import _collect_nonexistant_links


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
def _delete_all_pnbp(nb=None):
	""" if note contains #pnbp -> DELETE
	"""
	for n in nb.get_tagged("#pnbp"):
		lfn = n.name + '.md'
		if os.path.exists(os.path.join(nb.NOTE_PATH, lfn)):
			print(f'removing: {lfn} (#pnbp)')
			os.remove(os.path.join(nb.NOTE_PATH, lfn))


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
	ns = "\n#public posts:\n\n --- \n\n " + ns

	nb.generate_note('all public', ns, overwrite=True, pnbp=True)


@pass_nb
def _touch_all_public(nb=None):
	""" update the mod date for all #public """
	_collect_all_public(nb)

	for f in nb.notes['all public'].links:
		subprocess.run(['touch', os.path.join(nb.NOTE_PATH, f+'.md')])


@pass_nb
def _collect_terms(nb=None):
	""" if found [[TERMS]] -> nb/TERMS.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if n.is_linked('TERMS')])
	ns = "\nall [[TERMS]] :\n\n --- \n\n " + ns

	nb.generate_note('TERMS', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_unlinked(nb=None):
	""" if not a single [[]] found 
		-> nb/all unlinked.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if not n.links])
	ns = "\nall unlinked :\n\n --- \n\n " + ns

	nb.generate_note('all unlinked', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_empty(nb=None):
	""" if a note is created on path w/out context 
		-> nb/all empty.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if len(n.md) < 4])
	ns = "\nall empty :\n\n --- \n\n " + ns

	nb.generate_note('all empty', ns, overwrite=True, pnbp=True)


@pass_nb
def _delete_all_empty(nb=None):
	""" delete all empty notes from nb/all empty.md
	"""
	_collect_all_empty(nb) # refresh

	for l in nb.notes['all empty'].links:
		lfn = l + '.md'
		if os.path.exists(os.path.join(nb.NOTE_PATH, lfn)):
			print(f'removing: {lfn} (empty)')
			os.remove(os.path.join(nb.NOTE_PATH, lfn))


@pass_nb
def _collect_all_unheadered(nb=None):
	""" if not "Links: ..." at the first line, 
		-> nb/all unheadered.md
	"""
	ns = "".join([f"[[{n.name}]]\n" for n in nb.notes.values() if not n.header])
	ns = "\nall unheadered :\n\n --- \n\n " + ns

	nb.generate_note('all unheadered', ns, overwrite=True, pnbp=True)


@pass_nb
def _collect_all_moc(nb=None):
	""" "maps of content" via capitalization (e.g. [[PYTHON]]) 
		-> nb/all MOC.md
	"""
	ns = [n for n in nb.notes.values() if not n.is_tagged('#cont')]
	ns = [n for n in ns if n.is_tagged('#moc') or n.name.isupper()]
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










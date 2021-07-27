import re
import os
import subprocess

from pnbp.models import Note
from pnbp.wrappers import pass_nb
from pnbp.helpers import Link



""" 
"""
@pass_nb
def _strip_links_spacing(note:Note, nb=None):
	""" [[ LINK ]] -> [[LINK]]
	"""
	n = note
	p = re.compile(Link.MDS_INT_LNK)

	n.md_out = p.sub(Link.str_strip_link, n.md)
	n.save(nb)


@pass_nb
def _expand_links_spacing(note:Note, nb=None):
	""" [[LINK]] -> [[ LINK ]]
	"""
	n = note
	p = re.compile(Link.MDS_INT_LNK)

	n.md_out = p.sub(Link.str_expand_link, n.md)
	n.save(nb)


"""
"""
@pass_nb
def _prepend_leading_newline(nb=None):
	""" add (a single) '\n' if not to top of every note 
	""" 
	for n in nb.notes.values():
		if not n.md.startswith('\n'):
			n.md_out = '\n' + n.md
			n.save(nb)


@pass_nb
def _remove_leading_newline(nb=None):
	""" remove (a single) leading '\n' from every in note
		(->  it if you want consistant top of file)
	"""
	for n in nb.notes.values():
		if n.md.startswith('\n'):
			n.md_out = n.md[1:]
			n.save(nb)


@pass_nb
def _remove_leading_and_trailing_newlines(nb=None):
	""" str.strip() if necessary
	"""
	for n in nb.notes.values():
		if n.md.startswith('\n') or n.md.endswith('\n'):
			n.md_out = n.md.strip()
			n.save(nb)



""" 
"""
@pass_nb
def _link_unlinked_mentions(note:Note, nb=None):
	""" ...this is my favorite note -> this is [[my favorite note]]
	"""
	n = note

	n.prime_md_out_protect()
	ns = n.md_out
	nnames = sorted(nb.notes.keys(), reverse=True)
	
	# replace the unlinked mentions
	# within the .md text body:
	print(n.name, ':')
	for name in nnames:
		p = re.compile(fr'([^\[]\b)({name})(\b[^\]])')
		if (ml := p.findall(ns)):
			for m in ml:
				print(m[1], f'--> [[{m[1]}]]')
		ns = p.sub(Link.add_link_mention, ns)

	n.md_out = ns
	n.prime_md_out_release(nb) # saved in-line


@pass_nb
def _collect_unlinked_mentions(nb=None):
	""" ... -> nb/all unlinked mentions.md 
	""" # takes a long time ...
	nnames = sorted(nb.notes.keys(), reverse=True)
	ns = "\n\n---\n\n"
	for n in nb.notes.values():
		n.prime_md_out_protect()
		_md = n.md_out
		
		print(f'\n[[{n.name}]] :\n\t --> ')
		ns += f'\n[[{n.name}]] :'
		for name in nnames:
			p = re.compile(fr'([^\[]\b)({name})(\b[^\]])')
			if (ml := p.findall(_md)):
				ns += '\n\t --> '
				for m in ml:
					print(f'\[\[{m[1]}\]\], ')
					ns += f'\[\[{m[1]}\]\], '
		ns += '\n'
		n.md_out = ''
		n.pprotect = {}
		# ^^ not saving, just looking

	nb.generate_note('all unlinked mentions', ns, overwrite=True, pnbp=True)



"""
"""
@pass_nb
def _remove_nonexistant_links(note=Note, nb=None):
	""" [[An Old Note]] link -> An Old Note link
	"""
	n = note

	remv = []
	for name in n.links:
		if not nb.get(name):
			remv.append(name)

	n.remove_links(remv)
	print(n.md_out)
	n.save(nb)



""" 
"""
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
def _delete_all_empty(nb=None):
	""" delete all empty notes from nb/all empty.md
	"""
	for l in nb.notes['all empty'].links:
		lfn = l + '.md'
		if os.path.exists(os.path.join(nb.NOTE_PATH, lfn)):
			print(f'removing: {lfn} (empty)')
			os.remove(os.path.join(nb.NOTE_PATH, lfn))


@pass_nb
def _touch_all_public(nb=None):
	""" update the mod date for all #public 
	"""
	for pub in [n.name+'md' for n in nb.get_tagged(nb.COMMIT_TAG)]:
		subprocess.run(['touch', os.path.join(nb.NOTE_PATH, pub)])











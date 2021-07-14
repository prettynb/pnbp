import re

from pnbp.models import Note
from pnbp.wrappers import pass_nb
from pnbp.helpers import Link


"""
"""
@pass_nb
def _fix_link_spacing(note:Note, nb=None):
	""" [[ LINK ]] -> [[LINK]]
	"""
	n = note
	p = re.compile(Link.MDS_INT_LNK)

	n.md_out = p.sub(Link.str_strip_name, n.md)
	n.save(nb)


@pass_nb
def _add_leading_newline(nb=None):
	""" add '\n' if not to top of note 
	""" 
	for n in nb.notes.values():
		if not n.md.startswith('\n'):
			n.md_out = '\n' + n.md
			n.save(nb)


@pass_nb
def _remove_leading_newline(nb=None):
	""" remove leading '\n' if in note
	"""
	for n in nb.notes.values():
		if n.md.startswith('\n'):
			n.md_out = n.md[1:]
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

	nb.generate_note('all unlinked mentions', ns, overwrite=True)




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

	nb.generate_note('all nonexistant links', ns, overwrite=True)















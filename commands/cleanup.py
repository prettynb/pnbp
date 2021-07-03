import re

from pnbp.models import Note
from pnbp.wrappers import arrow_call, pass_nb
from pnbp.helpers import str_strip_link, add_link_mention


"""
"""
@pass_nb
def _fix_link_spacing(nb=None):
	""" [[ LINK ]] -> [[LINK]]
	"""
	p = re.compile(nb.MDS_INT_LNK)

	for n in nb.notes.values():
		if n.name == 'test1':
			n.md_out = p.sub(str_strip_link, n.md)
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

	pb = {}
	ns = n.md
	# pull out all code, links, tags, urls, 
	# so that they don't get matched with 
	for i, cb in enumerate(n.cblocks):
		_repl = f'cb_{i}.'
		ns = ns.replace(cb, _repl)
		pb.update({_repl: cb})
	for i, l in enumerate(n.links):
		_repl = f'l_{i}.'
		ns = ns.replace(f'[[{l}]]', _repl)
		pb.update({_repl: f'[[{l}]]'})
	for i, t in enumerate(n.tags):
		_repl = f't_{i}.'
		ns = ns.replace(t, _repl)
		pb.update({_repl: t})
	for i, u in enumerate(n.urls):
		_repl = f'u_{i}.'
		ns = ns.replace(u, _repl)
		pb.update({_repl: u})	

	nnames = sorted(nb.notes.keys(), reverse=True)
	
	# replace the unlinked mentions
	# within the md text body:
	print(n.name, ':')
	for name in nnames:
		p = re.compile(fr'([^\[]\b)({name})(\b[^\]])')
		if (ml := p.findall(ns)):
			for m in ml:
				print(m[1], f'--> [[{m[1]}]]')
		ns = p.sub(add_link_mention, ns)

	for k,v in pb.items():
		# put code, links, tags, urls, back in:
		ns = ns.replace(k, v)

	# save the note:
	n.md_out = ns
	n.save(nb)


@pass_nb
def _remove_nonexistant_links(note=Note, nb=None):
	""" [[An Old Note]] link -> An Old Note link
	"""
	remv = []
	for name in note.links:
		if not nb.get(name):
			remv.append(name)

	note.remove_links(remv)
	print(note.md_out)
	note.save(nb)










from string import ascii_uppercase

import click 

from pnbp.models import Notebook, Note
from pnbp.wrappers import pass_nb

""" -> graph 
	e.g. 

	```mermaid
		graph LR;
		
		A[hello-my-name-is]
		B[world22]
		AA[hola]
		AAAAAAAA[hi-again]
		
		A --> B
		B --> A
		AA --> A
	```
"""

@pass_nb
@click.option('--tag', help="The name of the #tag to be graphed. (#tag or tag)")
def _create_tag_graph(tag: str, nb=None):
	""" --tag -> nb/graph-tag-{tag}.md
	"""
	tag = tag.strip('#')

	ll = [ch for ch in ascii_uppercase] # link letters

	for i in range(2, 31): # support ~800 notes here (but mermaid might break)
		ll += [c*i for c in ascii_uppercase] # -> "AA", ... -> "AAA", ... -> 

	nnames = [n.slugname for n in nb.notes.values() if n.is_tagged(tag)]

	nameMvar = {nnames[i]:ll[i] for i in range(len(nnames))} # "all-public": "AAAA"

	outstr = f"#{tag}\n\n```mermaid\n\tgraph TD;"

	for k, v in nameMvar.items():
		outstr += f"\n\t{v}[{k}]" # set variables 

	for fn,n in nb.notes.items():
		if n.is_tagged(tag):
			sv = nameMvar[n.slugname]
			for li in n.links:
				if (n := nb.get(li)):
					if n.slugname in nnames:
						if n.is_tagged(tag):
							rv = nameMvar[n.slugname]
							outstr += f"\n\t{sv} --> {rv}" # link from variables 

	outstr += "\n```" # close md code block
	print(outstr)
	# print(len(outstr)) # wonder when it breaks
	nb.generate_note(f'graph-tag-{tag.strip("#")}', outstr, overwrite=True)


@pass_nb
def _collect_public_graph(nb=None):
	""" #public -> flat link graph notebook/graph-tag-public.md"""
	_create_tag_graph('public', nb)
	n = nb.get('graph-tag-public')
	n.append_section('\n#pnbp')
	n.save(nb)



@pass_nb
def _create_link_graph(note: Note, nb=None):
	""" --note	-> nb/graph-{note}.md 
	"""
	name = note.name

	ll = [ch for ch in ascii_uppercase] # ["A", "B", "C", ...]

	for i in range(2, 31): # support ~800 notes here (but mermaid might break)
		ll += [c*i for c in ascii_uppercase] # -> "AA", ... -> "AAA", ... -> 

	_nts = [n for n in nb.notes.values() if n.is_linked(name)]
	nnames = [n.slugname for n in _nts]

	nameMvar = {nnames[i]:ll[i] for i in range(len(nnames))} # "all-public": "AAAA"

	outstr = f"[[{name}]]\n\n```mermaid\n\tgraph TD;" # open md code block

	for k, v in nameMvar.items():
		outstr += f"\n\t{v}[{k}]" # set variables 

	for fn,n in nb.notes.items():
		if n.is_linked(name):
			sv = nameMvar[n.slugname]
			for li in n.links:
				if (n := nb.get(li)):
					if n.slugname in nnames:
						if n.is_linked(name):
							rv = nameMvar[n.slugname]
							outstr += f"\n\t{sv} --> {rv}" # link from variables 

	outstr += "\n```\n" # close md code block
	# print(outstr)
	# print(len(outstr)) # wonder when it breaks

	outstr += "\n--- \n"
	
	for n in _nts:
		# add the clickable links at the bottom of the note:
		outstr += f"\n[[{n.name}]]"
	
	nb.generate_note(f'graph-{name}', outstr, overwrite=True)



@pass_nb
def _collect_all_graphs(nb=None):
	""" if ```mermaid``` [[]] -> nb/all graphs.md
	"""
	ns = "\n\n--- \n"
	
	glnks = {}
	for n in nb.notes.values():
		_graph = False
		if n.name.startswith('graph-'):
			_graph = True
			glnks.update({f"[[{n.name}]]\n": _graph})

		if not _graph:
			for cb in n.codeblocks:
				if cb.codeblock.startswith('mermaid'):
					glnks.update({f"[[{n.name}]]\n": _graph})

	gs = [k for k,v in glnks.items() if not v]
	_gs = [k for k,v in glnks.items() if v]

	for g in _gs:
		ns += g

	ns += "\n\n--- \n"

	for g in gs:
		ns += g

	nb.generate_note('all graphs', ns, overwrite=True)



@pass_nb
def _delete_all_graph_dash_name(nb=None):
	"""
	"""
	for n in nb.notes.values():
		if n.name.startswith('graph-') and n.codeblocks[0].lang == 'mermaid':
			lfn = n.name + '.md'
			if os.path.exists(os.path.join(nb.NOTE_PATH, lfn)):
				print(f'removing: {lfn} (graph-)')
				os.remove(os.path.join(nb.NOTE_PATH, lfn))











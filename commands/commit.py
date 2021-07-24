import datetime
import subprocess
import os
import re

import click 

from pnbp.wrappers import pass_nb
from pnbp.helpers import _convert_datetime



@pass_nb
def _git_commit_notebook(nb=None):
	""" commit to local git -> nb/.git/
	"""
	st = subprocess.run(['git', '-C', nb.NOTE_PATH, 'status'], capture_output=True)
	print(st)

	if st.stderr == b'fatal: not a git repository (or any of the parent directories): .git\n':
		print(subprocess.run(['git', '-C', nb.NOTE_PATH, 'init'], capture_output=True))

	lt = datetime.datetime.strftime(datetime.datetime.now(), '%X')
	ld = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

	print(subprocess.run(['git', '-C', nb.NOTE_PATH, 'add', '-A'], capture_output=True))
	print(subprocess.run(['git', '-C', nb.NOTE_PATH, 'commit', '-m' , f'Automated commit @ {lt} on {ld}'], capture_output=True))



@pass_nb
def _collect_git_diff(nb=None):
	""" git diff -> nb/all diff.md
	"""
	FI_LI = r'diff --git a/(.+) b/(.+)'
	A_LI = r'--- a/(.+)'
	B_LI = r'\+\+\+ b/(.+)'

	res = subprocess.run(['git', '-C', nb.NOTE_PATH, 'diff'], capture_output=True)
	if (diff := res.stdout.decode('utf-8').strip()):
		res = diff
	else:
		return res.stderr.decode('utf-8').strip()

	diff_dict = {}
	curr = ''
	a = [] # -#
	b = [] # +
	
	dlen = len(res.splitlines())
	for i, dl in enumerate(res.splitlines()):

		if (m := re.match(FI_LI, dl)) or i == dlen-1:
			# start of a new file diff
			if curr and (a or b):
				diff_dict.update({curr: [a, b]})

			if not i == dlen-1:
				curr = m.group(1)
				a = []
				b = []

		if curr:
			if dl.startswith('-') and not re.match(A_LI, dl):
				if len(dl) > 1:
					if dl[1:].strip() == '---':
						a.append('\\' + dl[1:])
					else:
						a.append(dl[1:])
			elif dl.startswith('+') and not re.match(B_LI, dl):
				if len(dl) > 1:
					if dl[1:].strip() == '---':
						b.append('\\' + dl[1:])
					else:
						b.append(dl[1:])

	dt = _convert_datetime("now")
	ns = f"\ngit diff: ({dt})\n\n--- \n\n"
	for k,v in diff_dict.items():
		ns += f"#### [[{k.replace('.md', '')}]]\n"
		ns += '**ADDED**: \n{}\n\n\n'.format("\n".join(v[1]))
		ns += '**REMOVED**: \n{}\n\n--- \n\n'.format("\n".join(v[0]))

	nb.generate_note('all diff', ns, overwrite=True)



""" 
"""
@click.option('--path', default='.', help='File path to project directory')
def _init_git_ignore(path):
	""" write .gitignore w/ essentials to curr directory or --path specified
	"""
	defaultTxt = """.DS_Store
**__pycache__/**
*.sqlite3
*.sublime-*
*.pkl
*.py[co]
**/migrations/0*.py
*egg-info/**
settings.json
.env
	"""
	with open(os.path.join(path, '.gitignore'), 'w') as gitignore:
		gitignore.write(defaultTxt)
		
	click.echo(f'.gitignore --> {path}')










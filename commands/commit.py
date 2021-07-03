import datetime
import subprocess
import os

import click 

from pnbp.wrappers import pass_nb, arrow_call



@arrow_call
@pass_nb
def _git_commit_notebook(nb=None):
	""" commit to local git
	"""
	st = subprocess.run(['git', '-C', nb.NOTE_PATH, 'status'], capture_output=True)
	print(st)

	if st.stderr == b'fatal: not a git repository (or any of the parent directories): .git\n':
		print(subprocess.run(['git', '-C', nb.NOTE_PATH, 'init'], capture_output=True))

	lt = datetime.datetime.strftime(datetime.datetime.now(), '%X')
	ld = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

	print(subprocess.run(['git', '-C', nb.NOTE_PATH, 'add', '-A'], capture_output=True))
	print(subprocess.run(['git', '-C', nb.NOTE_PATH, 'commit', '-m' , f'Automated commit @ {lt} on {ld}'], capture_output=True))


# @pass_nb
# def _collect_git_diff(nb=None):
# 	""" not worth having -> parse it later?
# 	"""
# 	ns = subprocess.run(['git', 'diff', '-C', nb.NOTE_PATH], capture_output=True).stdout.decode('utf-8').strip()
# 	nb.generate_note('all diff', ns, overwrite=True)


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





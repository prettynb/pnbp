import json
import os
import subprocess

import click

from pnbp.wrappers import pass_nb



""" w/ symlink to NOTE_PATH
"""
@click.option('--path', default='.', help='File path to new project')
@pass_nb
def _subl_init(path, nb=None):
	""" Command to initiate local Sublime Text project 
		&& symlink it to the main nb directory
	"""
	defaultJson = {
		"folders":
		[
			{
				"follow_symlinks": True,
				"path": ".",
				"folder_exclude_patterns": ["__pycache__"],
			}
		],
		"settings": {
			"python_virtualenv": nb.VENV_PATH,
			"python_interpreter": f"{nb.VENV_PATH}/bin/python",
			"python_package_paths": [
			]
		}
	}

	if path == '.':
		path = os.getcwd()

	projname = path.split('/')[-1]

	with open(os.path.join(path, f'{projname}.sublime-project'), 'w') as f:
		f.write(json.dumps(defaultJson, indent=4))

	x = subprocess.run(['ln', '-s', os.path.join(path, f'{projname}.sublime-project'), nb.NOTE_PATH], capture_output=True)
	click.echo(x)

	_collect_subl_projs(nb)



""" ... 
"""
@pass_nb
def _collect_subl_projs(nb=None):
	""" nb/example.sublime_project -> sublime-project.md
		(via ![[example.sublime_project]])
	"""

	projs = []
	for fn in os.listdir(nb.NOTE_PATH):
		if fn.endswith('.sublime-project'):
			projs.append(fn)

	nmd = "\n\n".join([f'![[{p}]]' for p in projs])

	nb.generate_note('sublime-project', nmd, overwrite=True, pnbp=True)










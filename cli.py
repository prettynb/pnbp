import os 
import subprocess
import sys
import inspect

import click

from pnbp.models import Notebook
from pnbp.wrappers import arrow_call

from commands import collect as coll
from commands import commit as comm
from commands import correct as corr
from commands import code
from commands import graph
from commands import pprint
from commands import subl
from commands import tasks



@click.group()
def cli():
	pass


""" 
"""
def _nb_get_help():
	""" show the cli.py --help message 
	"""
	# providing access to the full installed --help list ...
	# note how documentation strings don't
	# pass into the command when built below
	loc_p = os.path.dirname(__file__)
	cli_p = os.path.join(loc_p, 'cli.py')
	
	click.echo(subprocess.run(['python3', cli_p, '--help']))


@cli.command()
def nb_get_help():
	_nb_get_help()




""" pnbp-blog api connection commands:
"""
@cli.command()
def nb_commit_html():
	""" if note contains #public, -> HTML_PATH/.html 
		(for local debugging when running remote server 
		and not a concurrent localhost instance...)
	"""
	# ^^ docstring == help message
	nb = Notebook()
	nb.write_commits_to_local_html()


@cli.command()
def nb_commit_remote():
	""" if note contains #public, -> 
		selective update POST to pnbp-blog api
		@ {API_BASE}/api/publishment
	"""
	nb = Notebook()
	nb.post_commits_to_blog_api()


@cli.command()
def nb_commit_local():
	""" commit -> localhost pnbp-blog instance
	""" # a convenience command
	nb = Notebook()
	nb.API_BASE = 'http://127.0.0.1:8000'
	nb.post_commits_to_blog_api()


@cli.command()
def nb_commit_stage():
	""" *only* print nb-commit- changes against nb.API_BASE
		to the terminal (staging view)
	"""
	nb = Notebook()
	nb.post_commits_to_blog_api(stage_only=True)


@cli.command()
def nb_commit_settings():
	""" *only* print nb-commit- changes against nb.API_BASE
		to the terminal (staging view)
	"""
	nb = Notebook()
	nb.blog_settings_post()


@cli.command()
def nb_git_clone_pnbp_blog():
	""" command to clone from github to a new blog/
	"""
	op = subprocess.run([
		'git', 'clone',
		'https://github.com/prettynb/pnbp-blog',
		'blog'
		],
		capture_output=True)

	if op.stdout:
		click.echo(op.stdout)
	else:
		click.echo(op.stderr)



""" building click.commands out of 
	the (imported above) local /commands/ package
"""
def _create_command(func):
	""" effectively writes a :

		```@click.command()
			def outer_act_cmd():
				_outer_act_cmd()
		```	

	where I had issues passing live parameters 
	and chaining command calls in click otherwise.
	
	As actively wrapping here (vs calling _outer_act_cmd()),
	has the nice feature of passing the _cmd's docstring to the --help info.

	:param func: 
	"""
	func.__name__ = func.__name__.lstrip('_')

	if not func.__name__.startswith('nb'):
		func.__name__ = f'nb_{func.__name__}'

	cmd = cli.command()

	if 'note' in inspect.signature(func).parameters.keys():
		# prove it : 
		func.__name__ = f'nbn_{func.__name__[3:]}'
		func = click.option('-n', '--note', type=str, help='the name of a note', required=True)(func)

	func = arrow_call(func)

	return cmd(func)


def create_command(func):
	""" actually instantiating the command
		and specifically setattr-ing here after built is necessary

	:param func: 
	"""
	c = _create_command(func)
	setattr(sys.modules[__name__], func.__name__.lstrip('_'), c)


def create_commands(module, _all=False):
	""" 

	:param module: an commands/module.py imported above
	:param _all: _all=True will create a command from all leading underscore _func_name of module
	"""
	for k,v in module.__dict__.items():
		# print(k) # _func's name...
		if _all:
			if inspect.isfunction(v) and k.startswith('_'):
				create_command(v)
		else:
			# leave open for additional bool switches
			pass



def create_all_commands():
	""" main function for building imported module commands 
		and tacking them onto the click.group(), & module local() name cli

	"""
	create_commands(coll, _all=True)

	create_commands(comm, _all=True)

	create_commands(corr, _all=True)


	create_command(code._extract_code_blocks)
	create_command(code._extract_all_code_blocks)

	create_command(graph._create_link_graph)
	create_command(graph._create_tag_graph)
	create_command(graph._delete_all_graph_dash_name)

	create_command(pprint._nb_pprint)

	create_command(subl._subl_init)

	create_command(tasks._nb_task_settle)



	








# -> required to call here (pre-main) for setup.py / 
# pip install to recognize dynamically created commands
create_all_commands()

if __name__ == '__main__':
	cli()
	






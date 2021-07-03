from setuptools import setup, find_namespace_packages

from click import Command

import cli


entry_points = '[console_scripts]'

for v in cli.__dict__.values():
	if isinstance(v, Command):
		if not (name := v.__dict__['name']) == 'cli':
			fxn_name = name.replace('-', '_')
			entry_points += f'\n{name}=cli:{fxn_name}'


setup(
	name='pnbp',
	version='0.7.0',
	py_modules=['cli'],
	install_requires=[
		'Click',
		'markdown',
		'requests'
	],
	entry_points=entry_points,
	package_dir={"pnbp": "pnbp"},
	packages=find_namespace_packages(),
)






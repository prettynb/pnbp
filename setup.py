from setuptools import setup, find_namespace_packages

# import click

import cli

entry_points = '[console_scripts]'

for v in cli.__dict__.values():
	# if isinstance(v, click.Command):
	if str(type(v)) == '<class \'click.core.Command\'>':
		if not (name := v.__dict__['name']) == 'cli':
			fxn_name = name.replace('-', '_')
			entry_points += f'\n{name}=cli:{fxn_name}'

import __license__ as about

setup(
	name=about.__title__,
	version=about.__version__,
	author=about.__author__,
	author_email=about.__author_email__,
	description=about.__description__,
	long_description=f'{about.__url__}/blob/master/README.md',
	long_description_content_type='text/markdown',
	url=about.__url__,
	license=about.__license__,
	project_urls={
	        'Source': about.__url__,
   	        'Documentation': f'{about.__url__}/blob/master/README.md',
		},
	classifiers=[
	        "Programming Language :: Python :: 3",
	        f"License :: OSI Approved :: {about.__license__}",
	        "Operating System :: OS Independent",
	    ],
	py_modules=['cli'],
	install_requires=[
		'Click>=7.1.2',
		'Markdown>=3.3.4',
		'requests>=2.26.0',
		'rich>=10.6.0'
	],
	entry_points=entry_points,
	package_dir={"pnbp": "pnbp"},
	packages=find_namespace_packages(),
	python_requires=">=3.6", #f-strings
)






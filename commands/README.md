**commands**

--- 

**core** : 

| cmd | desc |
| :----: | :----: |
| **nb-get-help** | if installed correctly, a list of available commands |
| **nb-collect-all** | |
| **nb-delete-all-pnbp** | if note contains #pnbp -> DELETE |
| ... | ... |
| nb-collect-unlinked-mentions | ... -> nb/all unlinked mentions.md |
| nb-delete-all-graph-dash-name | ... |

--- 

**correct** : 

| cmd | desc |
| :----: | :----: |
| nb-delete-all-empty | delete all empty notes from nb/all empty.md |
| ... | ... |
| nb-prepend-leading-newline | add '\n' if not to top note |
| nb-remove-leading-newline | remove '\n' if exists from top note |
| nb-remove-leading-and-trailing-newlines | ... | 
| ... | ... |
| nbn-strip-links-spacing | \[\[ LINK \]\] -> \[\[LINK\]\]  |
| nbn-expand-links-spacing | \[\[LINK\]\] -> \[\[ LINK \]\]  |
| ... | ... |
| **nbn-link-unlinked-mentions** | here is my favorite note -> here is my \[\[favorite note\]\] |
| **nbn-remove-nonexistant-links** | \[\[An Old Note\]\] link -> An Old Note link |

--- 

**commit** :

| cmd | desc |
| :----: | :----: |
| **nb-git-commit-notebook** | commit to local git |
| nb-collect-git-diff | git diff -> nb/all diff.md |

--- 

**-> pnbp-blog** :

| cmd | desc |
| :----: | :----: |
| **nb-git-clone-pnbp-blog** | command to clone from github to a new blog/ |
| nb-commit-remote | post #public to nb.API_BASE |
| nb-commit-local | post #public to localhost:8000 regardless nb.API_BASE |
| nb-commit-html | save the nb->html conversion to nb.HTML_PATH (local debug) |
| nb-commit-stage | *only* print nb-commit- changes against nb.API_BASE (staging view) |
| nb-touch-all-public | update the mod date for all #public (remote debug) |

--- 

#### **more commands** : 

--- 

**collect.py**

| cmd | desc |
| :----: | :----: |
| **nb-collect-all** |  perform all collect- commands in succession |
| nb-collect-all-empty | if a note is created on path w/out context ->... |
| nb-collect-all-moc | "maps of content" via capitalization (e.g. \[\[PYTHON\]\]) |
| nb-collect-all-notes | all .md files linked -> nb/all notes.md |
| nb-collect-all-public | if note contains #public -> nb/all public.md |
| nb-collect-all-stats | stats (incl [[links]] to  nb-collect-all "all \*" entries) |
| nb-collect-all-tags | a fancy generated note showing \#tag per \[\[\]\] (and \[\[\]\] per \#tag)  |
| nb-collect-all-unheadered | if not "Links: ..." at the first line, -> nb/all unheadered.md |
| nb-collect-all-unlinked | if not a single \[\[\]\] found -> nb/all unlinked.md |
| nb-collect-all-urls |  all regex-ed http-based urls -> nb/all urls.md |
| nb-collect-subl-projs | nb/example.sublime_project ->... |
| nb-collect-tasks-note | if \#tasks -> [[tasks]] |
| nb-collect-terms | if found [[TERMS]] -> nb/TERMS.md |
| nb-collect-code-blocked | if \`\`\`lang \`\`\` -> nb/all code blocked.md | 
| nb-collect-all-graphs | if \`\`\`mermaid \`\`\`, \[\[\]\] -> nb/all graphs.md |
| nb-collect-public-graph | \#public -> flat link graph...  |
| nb-collect-git-diff | git diff -> nb/all diff.md |
| nb-collect-nonexistant-links | ... -> nb/all nonexistant links.md |

... :
- ```nb-collect-all``` is a main command to call **that generates** a series of .md files to the **nb.NOTE_PATH**
- **nb/all stats.md** is one that \[\[links\]\] to all **\#pnbp** tag mentions.
- ```nb-delete-all-pnbp``` **will delete** every **\#pnbp** tagged .md file.
- **\#pnbp** tagged .md notes will all express as having : 
	- ```n.tags = [Tag(#pnbp)]```, ```n.links = []```,  ```n.codeblocks = []```, ```n.urls = []```.
- ^^ this ensures that any packaged command .md files produced to your **NOTE\_PATH** : 
	- (a) can be quickly bulk removed, 
	- (b) aren't referenced *themselves* among notes (and rather, just be abstracted collections of \[\[links\]\], \#tags, etc.); **we don't want** : 
		- ... ```nb-collect-all-tags``` -> **nb/all tags.md** reporting *itself* as having every single **\#tag**
		- ... **'all tags'** to show up in this: ```nb.get_tagged('#mytag')```
		- ... **'all notes'** in this: ```nb.get_linked('SCIENCE')```

```collect-all-moc```
- MOCs (*"Maps of Content"* ) ~= notes that mostly contain reference links to other notes (i.e. the *"content"* itself).
- By default, any note with an n.name that is "**ENTIRELY UPPERCASE**" is considered to be an MOC here. 
	- e.g. (default) **nb/HOME.md** would be an MOC, **nb/home.md** wouldn't be; 
	- ... if note **'HOME'** was tagged with **\#cont**, it *wouldn't* be considered an MOC
	- ... if note **'home'** was tagged with **\#moc**, it *would* be considered an MOC

-> personalize w/ **pnbp\_config.json** (default values shown here) :
	- ```"MOC_TAG": "#moc"``` -> explicit **\#tag** to *include* note to MOCs
	- ```"CONT_TAG": "#cont"``` -> explicit **\#tag** to *exclude* as MOC

```json
	...
	"MOC_TAG": "#map",
	"CONT_TAG": "#nam",
	...
```



---

**tasks.py**  

| cmd | desc |
| :----: | :----: |
| **nb-task-settle** | ... | 


```nb-task-settle```  

e.g. **note**(s) tagged **\#tasks** : 
- complete and **uncheck** 
	- *basic* (e.g. - \[x\] ex task -> - \[ \] ex task)
	- *parameterized* (e.g. -\[x\] water (amt:2c) ->  -\[ \] water (amt: )
- complete and ***remove*** 
	- *bulleted* (e.g. - todos marked as **\#complete** ->  )
- **record** completes
	- ... to **nb\/_complete.md** under a generated section w/ today's date.

-> personalize w/ **pnbp\_config.json** (default values shown here) :
- ```"TASKS_TAG": "#tasks"``` - the \#tag denoting that a note contains "tasks".
- ```"COMPL_TAG": "#complete"``` - the \#tag denoting that a bulleted line (within a note containing \#tasks) should be recorded to nb.NOTE_PATH/\_complete.md and removed from the note.
- ```"SCHED_TAG": "#schedule"``` - (under construction)
- ```"TASKS_NOTE": "tasks"``` - a .md file name for pnbp to save a list of \[\[note\]\] links for each that contain \#tasks.
- ```"COMPL_NOTE": "_complete"``` - a .md file name for pnbp to save bulleted tasks to, on **nb-task-settle** 

```json
	... 
	"TASKS_TAG": "#todos",
	"COMPL_TAG": "#compl",
	"COMPL_NOTE": "_compl",
	... 
```

--- 

**graph.py**

| cmd | desc |
| :----: | :----: |
| **nbn-create-link-graph** | -> nb/graph-{note}.md | 
| **nb-create-tag-graph** | --tag -> nb/graph-tag-{tag}.md |

generating flat relationship graphs to .md using **[mermaid js](https://mermaid-js.github.io/mermaid/#/)** : 

```nbn-create-link-graph -n SCIENCE```
- e.g. includes (and relates) every note **\[\[linked\]\]** within **nb/SCIENCE.md**, as well as every note that *backlinks* to **\[\[SCIENCE\]\]** (i.e. ```n.is_linked("SCIENCE")==True```);
- producing an **\`\`\`mermaid \`\`\`** graph to **nb/graph-SCIENCE.md**. 

```nb-create-tag-graph -t #mytag``` 
- e.g. includes every note tagged **\#mytag** (i.e. ```n.is_tagged("#mytag")==True```) and relates among them; 
- producing an \`\`\`mermaid \`\`\` graph to **nb/graph-tag-mytag.md**.


--- 

**code.py**

| cmd | desc |
| :----: | :----: |
| **nbn-extract-code-blocks** | --lang -> nb.NOTE_PATH/code/ | 
| **nbn-extract-all-code-blocks** | -> nb.NOTE_PATH/code/ (per lang found) | 

```nbn-extract-code-blocks --note="examp note" --lang=py```
- e.g. for each **\`\`\`py \`\`\`** (in ```n.codeblocks```) -> **nb/code/examp note.py**

```nbn-extract-all-codeblocks -n SCIENCE```
- e.g. for every valid commands.code.**LANG_EXTS** found (in ```n.codeblocks```) 
- -> **nb/code/n.name.ext**

```
% nbn-extract-code-blocks -n SCIENCE -l py
% cd notebook/code
% python SCIENCE.py
Hello World!
```


--- 

**subl.py**

| cmd | desc |
| :----: | :----: |
| **nb-subl-init** | --path="." |

```nb-subl-init```
```nb-subl-init --path="/Users/alice/myproject"```
- (1) initiates a templated **.sublime-project** (json) file to the path
- (2) symlinks the (remote) **.sublime-project** to the **nb.NOTE\_PATH**
- -> on call to ```nb-collect-subl-projs```, **nb/sublime-project.md** contains links that can open in **Sublime Text** when clicked ( e.g. **!\[\[myproject.sublime-project\]\]** ... ). 

```
% mkdir myproject
% cd myproject
% nb-subl-init
```


--- 

**commit.py**

| cmd | desc |
| :----: | :----: |
| **nb-init-git-ignore** | --path="." |

```nb-init-git-ignore```
```nb-init-git-ignore --path="/Users/alice/myproject"```

Command to initiate a templated **.gitignore** file to the current working dir.
- that has nothing inherently to do with the **Notebook** (is available for general convenience).
- but, still starts with ```nb-```, as every packaged command does.

```
% mkdir myproject
% cd myproject
% nb-init-git-ignore
```

--- 

**pprint.py**

| cmd | desc |
| :----: | :----: |
| **nbn-pprint** |  ... | 

```nbn-pprint -n SCIENCE```
- e.g. rich print note to terminal ( ... )

see [pnano](https://github.com/prettynb/pnano) for more details.

--- 

___ 

### register new commands :

--- 

##### **intro** :
- -> ```nb-do-this-thing``` will be the resulting command (when registered).
- ```@pass_nb``` provides an instance of **Notebook**, if one isn't being provided.  
- w/ ```def _func_name(nb=None):``` (decorator + leading underscore +  default) tells you that the function will be registered as a **command** ( in ../cli.py ). 
- meaning, ```def func_name():``` here (as a general pattern) aren't.
- (note : using ```def _nb_do_this_thing(...``` will result in the same ```nb-do-this-thing``` command name. ) 

```py
# commands/new.py
from pnbp.wrappers import pass_nb


def some_portion(nb):
	pass

@pass_nb
def _do_this_thing(nb=None):
	# ...
	some_portion(nb)
	# ...
```

...  


##### **accepting a note by name** :
- -> ```nb-parse-these-thing -n SCIENCE```

```py
# commands/new.py
from pnbp.wrappers import pass_nb
from pnbp.models import Note

@pass_nb
def _parse_these_thing(note: Note, nb=None):
	pass
```

...  

##### **accept your own click options** :
-> ```nb-search-for -s "blah blah"```

```py
# commands/new.py
import click
from pnbp.wrappers import pass_nb

@pass_nb
@click.option('-s', '--search-str', help="a string to search for in the notebook.")
def _search_for(search_str: str, nb=None):
	ns = []
	for n in nb.notes.values():
		if search_str in n.md:
			ns.append(n)

	print(f"{search_str} found in {len(ns)} notes :")
	for n in ns:
		print(f"- {n.name}")
```

... 

##### pnbp=True -> 
nb.generate_note(..., **pnbp=True**)
- on ```pnbp=True```, the note.md is tagged **\#pnbp** (at the bottom).
- **ensuring that** : 
	- (a) no litter is left behind when calling ```nb-delete-all-pnbp```.
	- (b) it's **nb/all stats.md** collected.
	- (c) it's not littering your own (or anybody else's) matches when using e.g. :  ```n.is_tagged(...), n.is_linked(...)```, ```nb.get_tagged(...), nb.get_linked(...)```.
	- (d) ^^ it's not littering other **\#pnbp** (e.g. ... 
- every (currently) generated via ```nb-collect-all``` and ```nb-collect-unlinked-mentions```
- **user generated *w/* pnbp commands** are explicitly *not* **\#pnbp** : 
	- **graph.py** 's ```nb-create-link-graph```,  ```nb-create-tag-graph```, 
	- **tasks.py** used ```nb/_complete.md``` file,  
	- anything **code.py** extracted via```nb-extract-code-blocks``` or ```nb-extract-all-code-blocks``` to ```nb.NOTE_PATH/code/``` files.
- **ensuring that** :
	- ```nb-delete-all-pnbp``` doesn't remove things you likely want to keep. 
	- ```nb-collect-all-graphs``` (-> **nb/all graphs.md**) gives \[\[links\]\].
	- ... 

```py
@pass_nb
def _collect_something_new(nb=None):
	# ...
	nb.generate_note(name='new thing', md_out='...', overwrite=True, pnbp=True)
```


--- 

#### -> **[../cli.py](https://github.com/prettynb/pnbp/blob/master/cli.py)**


1. import your module from the commands package (at the top) :

```py
# ...
from commands import new
# ...
```

2. find and append to the ```create_all_commands()``` function : 

```py
# ... 
def create_all_commands():
	# ... 
	# add individually : 
	create_command(new._collect_something_new) # -> nb-collect-something-new
	# or by module :
	create_commands(new, _all=True) # _func -> nb-func 
# ... 
```

3. navigate to ```pnbp/``` and run ```pip install --editable .``` again : 

```py
(venv) % cd pnbp
(venv) % pip install --editable .
# ... 
(venv) % nb-get-help
# -> see your new command in the list !
(venv) % nb-do-this-thing
```

--- 
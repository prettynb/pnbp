pnbp = "pretty notebook parser"

Regex parsing models and extendable Click CLI tool to interact w/ an Extended/super-markdown [[wiki-link]] supported notebook (e.g. https://obsidian.md/) and the [pnbp-blog](https://github.com/prettynb/pnbp-blog/) API.


--- 
**installing pnbp**

```sh
git clone https://github.com/prettynb/pnbp/ pnbp
cd pnbp/
pip install -r requirements.txt
pip install --editable .
# ... 
nb-get-help # returns list of available cli commands packaged
```

set **NOTE_PATH** as an environment variable in your shell profile (e.g.

```sh
echo 'export NOTE_PATH="/users/alice/notebook"' >> ~/.zshrc
```
optionally set **IMG_PATH** and **HTML_PATH** as environment variables (values found here used before conf_file settings).
```sh
echo 'export IMG_PATH="$NOTE_PATH/imgs"' >> ~/.zshrc
echo 'export HTML_PATH="$NOTE_PATH/blogtest"' >> ~/.zshrc
```
)

next, set-up with an empty **NOTE_PATH/pnbp_conf.json** by instantiating your Notebook and following the prompt:
```py
>>> import pnbp
>>> nb = pnbp.Notebook()
... 
```

or, directly see conf_template.json -> write to NOTE_PATH/pnbp_conf.json, ignoring any personally unused values. e.g. minimal contents:

```json
{
    "IMG_PATH": "/users/alice/notebook/imgs",
    "API_BASE": "http://127.0.0.1:8000",
    "API_TOKEN": "fakeinitialvalue",
    "PUB_LNK_ONLY": false
}
```

Setting ```"PUB_LNK_ONLY": true``` turns off rendering for any internal links to HTML that are not of additionally published to a pnbp-blog instance (aka #public) notes.

You can ignore any creation of and values from NOTE_PATH/pnbp_conf.json by setting an environment variable **NOTE_CONFIG** to "off". This allows for a bare bones set-up for Notebook interaction without setting up any pnbp-blog config variables.

```sh
echo 'export NOTE_CONFIG="off"' >> ~/.zshrc
```

... 
\*\* If running on Windows, ensure that "\\" file paths are escaped (note: drive letter is only necessary if the directory isn't on your %HOMEDRIVE%):

```json
    ...
    "NOTE_PATH": "C:\\Users\\alice\\notebook",
    "IMG_PATH": "\\Users\\alice\\notebook\\imgs",
    ...
```

--- 
**the notebook + note models**:

```py
>>> import pnbp
>>> 
>>> nb = pnbp.Notebook()
>>> 
>>> # notes dict available
>>> nb.notes.values() # k=note name, v=pnbp.Note
>>> # get note directly by name
>>> n = nb.get('example note')
>>> # update content -> md_out
>>> n.md_out('this is the new contents of my note~!')
>>> # save it to the notebook
>>> n.save(nb) 
>>> # ...
>>> n = n.save(nb)
>>> # is equiv to 
>>> nb.get('example note')
>>> # meaning, nb holds live changes from n.save(),
>>> # but without "n =", if asked for n.md, would be the old pre-saved md
>>> # (aka n itself doesn't inplace so keep it or nb.get() it in the future)
>>> 
>>> # the note instance exposes:
>>> n.name #-> str, the name of the note (sans ".md")
>>> n.md #-> str, the actual file content
>>> n.links #-> list, the double-bracketed internal nb links
>>> n.tags #-> list, the #tags found (outside of any code, url, or \#escaped)
>>> n.urls #-> list, the http(s) external links 
>>> n.cblocks #->list, any blocks of code via triple-backtick 
>>> n.mtime #->str the file's modification date 
>>> 
>>> n.slugname # n.name=Example Note => n.slugname=example-note
>>> n.sections # the n.md str split at "---"
>>> n.header # -> bool, via looking for "Links: ..."
>>> 
>>> n.is_tagged('#egtag') # ->bool
>>> n.is_tagged(['#taga', '#tagb', '#tagc']) #-> True if any tags found
>>> n.is_tagged(['#taga', '#tagb', '#tagc'], to_all=True) #-> True if all found
>>> n.is_tagged(at_all=True) #-> True if tags in n.tags at all
>>> n.is_linked('example note') # ->bool
>>> n.is_linked(['note-a', '[[note-b]]', '[[ NoTE-C ]]']) # accept brackets and case-insensitive
>>> n.is_linked(['note-a', 'note-b', 'note-c'], to_all=True) # ... 
>>> n.is_linked(at_all=True) # ... 
>>> 
>>> # and others via the notebook instance:
>>> nb.get_tagged('#egtag') # ->n list
>>> nb.tags #-> list of all notebook found tags
>>> 
>>> nb.find(r'~!') #->n list, search notebook for regex 
>>> nb.find_and_replace(r'~!', '!!') # replace (be careful!!)
>>> # ... 
>>> nb.generate_note('examp note 2', 'more great content here...', overwrite=True)
```

--- 
**main avail commands:**        

| cmd | desc |
| :----: | :----: |
| **nb-get-help** | if installed correctly, recieve list of available installed commands |
| nb-commit-remote | post #public to nb.API_BASE |
| nb-commit-local | post #public to localhost:8000 regardless nb.API_BASE |
| nb-commit-html | save the nb->html conversion to nb.HTML_PATH (local debug) |
| ... | ... |
| nb-add-leading-newline | add '\n' if not to top note |
| nb-remove-leading-newline | remove '\n' if exists from top note |
| nb-fix-link-spacing | \[\[ LINK \]\] -> \[\[LINK\]\]  |
| nb-link-unlinked-mentions | here is my favorite note -> here is my \[\[favorite note\]\] |
| nb-git-commit-notebook | commit to local git |

--- 
**more commands:**

---
**nb-task-settle**   

if a note contains \#tasks, complete and uncheck basic and parameterized "- \[x\] ex task"  ->  "-\[ \] ex task", "-\[x\] water (amt:2c)" ->  "-\[ \] water (amt: )", as well as remove bulleted "- todos marked as \#complete". All variants are recorded to [[\_complete]] under section w/ today's date.


--- 

**nb-collect-all**

generates these .md files to the nb/ : TERMS.md, all MOC.md, all code blocked.md, all empty.md, all graphs.md, all nonexistant links.md, all notes.md, all public.md, all stats.md, all tags.md, all unheadered.md, all unlinked.md, all unlinked mentions.md, graph-tag-public.md, ... via (individually available commands...):

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
| ... |  |
| **nb-delete-all-empty** | delete all empty notes from nb/all empty.md |
| **nb-touch-all-public** | update the mod date for all #public |


--- 

... 

--- 
**nb-pprint** --note="examp note"
rich print note to terminal ( ... )


--- 

**nb-extract-code-blocks** --note="examp note" --lang="py"
for each ```lang ``` in note -> nb/code/n.name.ext

**nb-extract-all-codeblocks** --note="examp note"
for each valid **LANG_EXTS** found -> nb/code/n.name.ext


--- 

**nb-subl-init** --path="."

Command to initiate a templated sublime-project.json file && symlink it to the main nb/ directory (-> clickable links to sublime projects at sublime-project.md).

--- 

**nb-init-git-ignore** --path="."

Command to initiate a templated .gitignore file to the current working dir.
This is a general convenience command and has nothing inherently to do with the Notebook. Still func named "nb-" to keep within packaged installed command namespace.

--- 










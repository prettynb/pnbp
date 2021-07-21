**commands**

--- 

**main available commands:**

| cmd | desc |
| :----: | :----: |
| **nb-get-help** | if installed correctly, a list of available commands |
| nb-commit-remote | post #public to nb.API_BASE |
| nb-commit-local | post #public to localhost:8000 regardless nb.API_BASE |
| nb-commit-html | save the nb->html conversion to nb.HTML_PATH (local debug) |
| nb-commit-stage | *only* print nb-commit- changes against nb.API_BASE (staging view) |
| ... | ... |
| nb-add-leading-newline | add '\n' if not to top note |
| nb-remove-leading-newline | remove '\n' if exists from top note |
| nb-fix-link-spacing | \[\[ LINK \]\] -> \[\[LINK\]\]  |
| nb-link-unlinked-mentions | here is my favorite note -> here is my \[\[favorite note\]\] |
| nb-git-commit-notebook | commit to local git |

--- 

**more commands:**

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
| nb-collect-all-graphs | |
| nb-collect-all-graphs | |
| nb-collect-public-graph | |
| nb-collect-unlinked-mentions | |
| nb-collect-nonexistant-links | |
| ... |  |
| **nb-delete-all-empty** | delete all empty notes from nb/all empty.md |
| **nb-touch-all-public** | update the mod date for all #public |
| **nb-collect-git-diff** | |

---

**nb-task-settle**   

if a note contains \#tasks, complete and uncheck basic and parameterized "- \[x\] ex task"  ->  "-\[ \] ex task", "-\[x\] water (amt:2c)" ->  "-\[ \] water (amt: )", as well as remove bulleted "- todos marked as \#complete". All variants are recorded to \[\[\_complete\]\] under section w/ today's date.

--- 

**nb-create-link-graph**

**nb-create-tag-graph**

--- 

**nb-pprint** --note="examp note"

rich print note to terminal ( ... )

see pnano for more details. 

--- 

**nb-extract-code-blocks** --note="examp note" --lang="py"
- for each ```lang ``` in note -> nb/code/n.name.ext

**nb-extract-all-codeblocks** --note="examp note"
- for each valid **LANG_EXTS** found -> nb/code/n.name.ext


--- 
--- 

**nb-subl-init** --path="."

Command to initiate a templated sublime-project.json file && symlink it to the main nb/ directory (-> clickable links to sublime projects at sublime-project.md).

--- 

**nb-init-git-ignore** --path="."

Command to initiate a templated .gitignore file to the current working dir.
This is a general convenience command and has nothing inherently to do with the Notebook. Still func named "nb-" to keep within packaged installed command namespace.

--- 

Register new commands (via modules) in **pnbp/cli.py**

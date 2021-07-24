pnbp = **"pretty notebook parser"**

--- 

**pnbp** provides programmatic access to a **notebook** via :
- **[> pnbp/pnbp](https://github.com/prettynb/pnbp/tree/master/pnbp)** : **models and methods**. 
    - access notes and their individual (regex established) components in the python repl, scripts, and your own shell commands. 
- **[> pnbp/commands](https://github.com/prettynb/pnbp/tree/master/commands)** : **shell commands**. 
    - run pre-defined function against a notebook in the terminal directly, or, scheduled.

\--- 

a pretty **notebook** is the collection of markdown files in a specific directory.
a pretty **note** is a single .md file within the notebook directory.

**links** ( \[\[link\]\] , !\[\[link.jpg\]\] ), **tags** ( \#tag ), **codeblocks** ( \`\`\`py print("Hello World")\`\`\` ), and **urls** ( \[goog\]\(https://google.com) ) are the main components outside of additional [render syntax](https://daringfireball.net/projects/markdown/syntax) of a .md note using an extended linking and tagging markdown. 

https://obsidian.md/ is the best example of this in action. 

--- 

#### quickstart guide : 

--- 

##### (1) -> **git clone** the repo.

```bash
git clone https://github.com/prettynb/pnbp/ pnbp
cd pnbp/
pip install -r requirements.txt
pip install --editable .
```

--- 

##### (2) -> set **environment variables**.

| var | desc | e.g. |
| :--: | :--: | :--: |
| **NOTE_PATH** | the full directory path of your notebook | ```echo 'export NOTE_PATH="/users/alice/notebook"' >> ~/.zshrc``` |
| **IMG_PATH** | (optional entirely; set here or in pnbp_conf.json) | ```echo 'export IMG_PATH="$NOTE_PATH/imgs"' >> ~/.zshrc``` | 
| **HTML_PATH** | (optional entirely; useful debug w/ pnbp-blog; set here, in pnbp_conf.json, or not at all.) | ```echo 'export HTML_PATH="$NOTE_PATH/html"' >> ~/.zshrc``` | 
| **NOTE_NESTED** | (optional; default=*"flat"*) => *"single"*, *"recurs"*, *"all"*,  | ... |
| **NOTE_CONFIG** | (optional) => **"off"** to ignore using a NOTE_PATH/pnbp_conf.json  | ```echo 'export NOTE_CONFIG="off"' >> ~/.zshrc``` |

**NOTE_NESTED**  
- *"flat"* - by default, **pnbp** assumes that every .md note exist within the base directory level of **NOTE\_PATH**/.
- *"single"* - if you want **pnbp** to search for .md notes within additional (non-hidden) directory level up.
- *"recurs"* - if you want .md notes to be found through all (non-hidden) directory levels up.
- *"all"* - if you want even hidden (non- .git, .obsidian) directories traversed recursively up.

**NOTE_CONFIG**  
- without ```NOTE_CONFIG="off"```, "**NOTE\_PATH/pnbp_conf.json**" will be nagged for.
- **Notebook** can generate one at the python prompt that you can edit later -> 

( ... on **Windows**? Environment Variable(s) can be set [here](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0). Also, recall that in most places you'll also need to escape the "```\```" within any **path** strings (e.g. ```"IMG_PATH": "\\Users\\alice\\notebook\\imgs"```) used; the drive letter (e.g. ```"D:\\Media\imgs"```) is optional if it's your **\%HOMEDRIVE\%**. )

--- 

##### (3) -> **access your notes in python3.9 !**


```py
>>> import pnbp
>>> nb = pnbp.Notebook()
... 
```

--- 










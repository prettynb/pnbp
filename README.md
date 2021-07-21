pnbp = **"pretty notebook parser"**

--- 

a pretty **notebook** is the collection of markdown files in a specific directory.
a pretty **note** is a single .md file within the notebook directory.

**links** ( \[\[link\]\] , !\[\[link.jpg\]\] ), **tags** ( \#tag ), **codeblocks** ( \`\`\`py print("Hello World")\`\`\` ), and **urls** ( \[goog\]\(https://google.com) ) are the main components outside of additional [render syntax](https://daringfireball.net/projects/markdown/syntax) of a .md note using an extended linking and tagging markdown. 

https://obsidian.md/ is the best example of this in action. 

**pnbp** provides programmatic access to a notebook via :
- **[pnbp/pnbp](https://github.com/prettynb/pnbp/tree/master/pnbp)** : contains models and methods. access your notes and update them live from the python repl, in scripts, or your own commands (easily). 
- **[pnbp/commands](https://github.com/prettynb/pnbp/tree/master/commands)** : contains shell commands. work with the notebook using packaged commands directly in the terminal, or, schedule them.


--- 

**installation** : 

(1)

```bash
git clone https://github.com/prettynb/pnbp/ pnbp
cd pnbp/
pip install -r requirements.txt
pip install --editable .
```

(2)

set **NOTE_PATH**, as an environment variable,  to the full directory path of your notebook

(e.g. macos/linux appending your sh profile: ```echo 'export NOTE_PATH="/users/alice/notebook"' >> ~/.zshrc```

or see more for **Windows** below).

(3)

set **NOTE_CONFIG** to "off" (e.g. ```echo 'export NOTE_CONFIG="off"' >> ~/.zshrc```) if you want to stop here and ignore the rest.

**IMG_PATH** and **HTML_PATH** can also optionally be understood as environment variables, e.g. 

```sh
echo 'export IMG_PATH="$NOTE_PATH/imgs"' >> ~/.zshrc
echo 'export HTML_PATH="$NOTE_PATH/blogtest"' >> ~/.zshrc
```

or set later.

If you don't use ```NOTE_CONFIG="off"```, when you open the notebook in python for the first time, you'll be prompted to a default **NOTE_PATH/pnbp_conf.json** generated that you can edit later on :

```py
>>> import pnbp
>>> nb = pnbp.Notebook()
... 
```

see **conf_template.json** (and [pnbp-blog](https://github.com/prettynb/pnbp-blog)'s README as most is associated).

Have fun.

--- 

**Windows** : 

\*\* When you set a file path, ensure that each "\\" is escaped  
(drive letter is only necessary if the directory isn't on your %HOMEDRIVE%):

```json
    ...
    "NOTE_PATH": "C:\\Users\\alice\\notebook",
    "IMG_PATH": "\\Users\\alice\\notebook\\imgs",
    ...
```

and here is an [oracle docs](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html) guide on Environment Variables. 


--- 








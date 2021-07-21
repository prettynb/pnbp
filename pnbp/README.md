
--- 

a **Notebook** instance contains a dictionary of each **Note** available by it's name :

```py
>>> import pnbp
>>> nb = pnbp.Notebook()
>>> nb.notes.values() # k=note name, v=pnbp.Note
>>> n = nb.notes['SCIENCE']
>>> n = nb.notes.get('SCIENCE')
```

best accessed directly from the nb with .get() :

```py
>>> # get by best match ~
>>> n = nb.get('sc13nce')
```

each note exposes lists of **Link**s, **Tag**s, **CodeBlock**s, **Url**s, (and more) :

```py
>>> n.name #-> str, the name of the note (sans ".md")
>>> n.md #-> str, the actual file content
>>> n.links #-> list, the str name of all double-bracketed internal [[links]] found
>>> n.tags #-> list, the #tags found (outside of any code, url, or \#escaped)
>>> n.urls #-> list, the http(s) external links 
>>> n.codeblocks #->list, any blocks of code via triple-backtick 
>>> n.mtime #->str the file's modification date 
>>> 
>>> n.slugname #->str n.name=Example Note => n.slugname=example-note
>>> n.sections #->list the n.md str split at "---"
>>> n.header # -> bool, via looking for "Links: ..."
```

 the **notebook** instance can provide collections of things: 

```py
>>> nb.get_tagged('#egtag') # ->n list
>>> nb.get_linked('SCIENCE') # ->n list
>>> nb.tags #-> list of all notebook found tags
>>> nb.links #-> list of all notes by name (is nb.notes.keys())
>>> nb.urls #-> list of all unique urls from all notes
```

and **note**(s) can be individually queried against things: 

```py
>>> n.is_tagged('#egtag') #->bool
>>> n.is_tagged(['#taga', '#tagb', '#tagc']) #-> True if any tags found
>>> n.is_tagged(['#taga', '#tagb', '#tagc'], to_all=True) #-> True if all found
>>> n.is_tagged(at_all=True) #-> True if tags in n.tags at all
>>> n.is_linked('example note') #->bool
>>> n.is_linked(['note-a', '[[note-b]]', '[[ NoTE-C ]]']) # accept brackets and case-insensitive
>>> n.is_linked(['note-a', 'note-b', 'note-c'], to_all=True) # ... 
>>> n.is_linked(at_all=True) # ... 
```

--- 
**update the contents of a note...** 


manually :

```py
>>> import pnbp
>>> 
>>> nb = pnbp.Notebook()
>>> # get note directly by name
>>> n = nb.get('example note')
>>> # update content -> md_out
>>> n.md_out = n.md + '\nappending an example line~!'
>>> # save it to the notebook
>>> n.save(nb) 
>>> # the nb holds the live changes from n.save(nb) inplace
>>> n = nb.get('example note')
>>> # and is eqivalent to 
>>> n = n.save(nb)
>>> # noting that n itself doesn't inplace
>>> # meaning,
>>> n.md_out = "entirely new"
>>> n.save(nb)
>>> n.md # n here is older than what's in the nb !
```

search and destroy :

```py
>>> nb.find(r'~!') #->n list, search notebook for regex 
>>> nb.find_and_replace(r'~!', '!!') # inline replacements (be careful!!)
>>> # ... 
>>> nb.find_and_replace("appending an example line!!", "")
```

prime content protected :

```py
>>> import re
>>> n = nb.get("SCIENCE")
>>> n.prime_md_out_protect()
>>> # inplace, n.md_out becomes n.md
>>> # but w/ all n.links, n.tags, n.urls, n.codeblocks
>>> # protected against change 
>>> # by being replaced with a string key e.g. l_01.
>>> n.md_out = re.sub(r'example', 'e.x.', n.md_out) # ... 
>>> n.prime_md_out_release() # l_01. -> [[example note]]
>>> n.save(nb)
>>> # or
>>> n.prime_md_out_release(nb) # inplace save
```

by section :

```py
>>> n = nb.get("SCIENCE")
>>> new_section = "The Scientific Method\n\nblah blah blah"
>>> n.append_section(new_section) # to the end
>>> n = n.save(nb)
>>> n.insert_section(0, "An added section by index")
>>> n = n.save(nb)
>>> n.prepend_section("Add to the beginning, but not before an n.header.")
>>> n.md_out = "" # nevermind, don't want that
>>> n.prepend_today_section(nb)
>>> # ^^ added section headered w/ YYYY-MM-DD
>>> # and saved inplace
```

generate a new note :

```py
>>> nb.generate_note(name='examp note 2', md_out='more *great* content here...')
>>> n = nb.get('examp note 2')
>>> n.md # from the new nb.NOTE_PATH/examp note 2.md
more *great* content here...
>>> # must overwrite=True if note exists (else throw error and no deal)
>>> nb.generate_note('example note', "**better** content", overwrite=True)
```

--- 

**Link**, **Tag**, **CodeBlock**, and **Url** all subclass pnbp.helpers.**Helper**. 

A **Helper** subclass produces a namedtuple object of it's own class name, with a single named instance variable of it's own class name (e.g. ```Link(link="SCIENCE")```, ```Tag(tag="#tag")```, ... ). 

In order to maintain simple access to them as though referencing against their string-ed value, the **Helper** class provides methods that make them shake hands as such : 

```py
>>> n = nb.get("SCIENCE")
>>> "#tag" in n.tags
True
>>> n.links[0] == "SCIENCE"
True
>>> n.links[0] + " *is* a linked note in n !"
"SCIENCE *is* a linked note in n !"
```

Each subclass definition holds it's own regex pattern, various string replacement methods, in addition to exposing class specific properties on instance :

```py
>>> n.tags[0] == "tag"
True
>>> n.links
['SCIENCE']
>>> [l.aslink for l in n.links]
['[[SCIENCE]]']
```

--- 
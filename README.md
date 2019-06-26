# Python 2nd course
My homework and some templates created in the last year.

Every folder has some kind of encoding:

- **Z _number_** - just task numeration, nothing special
- **_ind_** means individual task, _**coll**_ - collective 
(i.e. for all students the same)
- number like 25.2 after that is number of theme and task
in the .pdf file sent by our teacher
- if there's **_v_number_**, it identifies a number of my individual task,
variant number, I mean.
- after all, **_(1)_** means that in previous version
something was wrong, but I needed it. Working code
is usually in _xxx(1).py_, not in _xxx.py_   
- finally, if you see something like Govnocode or examples folder,
I'll disappoint you - there are only my bad attempts in the first 
kind of folders and some examples of my friends' and teachers'
code, recipes from cookbooks and snippets from Stackoverflow in the second.

Oh, completely forgotten. Sometimes code can contain dumb structures,
like class Person or kind of this. Sorry, but this class is not my fault. It's in
homework task specification... 

##SEM 1

- **z2, z3** - numpy library
- **z4** - matplotlib library + numpy
- **z5, z6** - regex using re library
- **z7** - os.path library

**_Boring:_** _System journal task_
This is some kind of system journal, nothing special

- **z8** - openpyxl library, works with MS Excel docs
- **z9, z10, z11** - tkinter library stuff

**_Less boring:_** _Football tournament results table_
(z10, ind)

**_Almost interesting:_** _MS Word document viewer_ 
using tkinter. Saves text size, font, color, 
bold/italic stuff and paragraphs
(z11, ind v11(1))

- **z13** - socket server with SQLite3 database

##SEM 2

- **z1** - socket library

**_Interesting:_** _ChatServer task_
This is simple server 
and client programs for making a chat using sockets

- **z2** - HTML parser (STL, BeautifulSoup)

**_Interesting:_** _Article tone analyzer_
Using GUI in Tkinter ;) You choose parser, author from 
news site and time interval. This piece of AI (no) says 
about positive tone of articles in a scale from -2 to 2.

- **z3** - CGI web app, just for fun :)
- **z4** - WCGI web app, it's a phone book using json
- **z5** - CGI & WSGI once again. 
Looks like we were doing tasks on JSON.


**_Less boring:_** _Football tournament results table_ (ind) 

- **z6** - XML

**_Less boring:_** _Currency exchange_ (ind)

- **z7, z8** - SQLite 3

**_Less boring:_** _Currency exchange_ once again, 
storing data in database (coll z8).

**_Less boring:_** _Railway simulator_ with broken CSS and
even static/ folder (ind z8)

- **z9** - unittest library

## TEMPLATES

This contains 2 files for copypasting into my homework:

#### **database.py**

Simple (and vulnerable because of formatting in SQL, so it can be harmed using injections)
database class, which contains several methods for SQLite3 DB

#### **format_resp.py**

Contains a function which performs _string.format()_, 
but with html file, which can contain css or stuff and ruin 
regular _.format()_ work.

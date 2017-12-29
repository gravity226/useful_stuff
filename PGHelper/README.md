## Postgres Helper
This class is meant to make working with Postgres a little bit easier.

## Table of Contents
1. [What you need](https://github.com/gravity226/useful_stuff/tree/master/PGHelper#what-you-need)
2. [Start using it](https://github.com/gravity226/useful_stuff/tree/master/PGHelper#start-using-it)
3. [Setting up your ~/.bash_profile (Mac only) ](https://github.com/gravity226/useful_stuff/tree/master/PGHelper#optional---setting-up-your-bash_profile-mac-only)
4. [Don't load everything into memory](https://github.com/gravity226/useful_stuff/tree/master/PGHelper#dont-load-everything-into-memory)

## What you need...
1. Works with Python 2.7

2. Download the files (PGHelper.py and requirements.txt)

3. Install requirements

```bash
pip install -r requirements.txt
```

## Start using it

- Standard use case
```Python
from PGHelper import PGHelper
import os

pg_helper = PGHelper(dbname=os.environ['db_name'],
                     host=os.environ['db_host'],
                     user=os.environ['db_user'],
                     password=os.environ['db_password'],
                     port=os.environ['db_port'])

results = pg_helper.execute_query(query='''select * from schema.table limit 1;''')
print results
```

- Using **with**, the DB connection will be closed automatically on completion
```Python
from PGHelper import PGHelper
import os

with PGHelper(dbname=os.environ['db_name'],
              host=os.environ['db_host'],
              user=os.environ['db_user'],
              password=os.environ['db_password'],
              port=os.environ['db_port']) as pg_helper:
    results = pg_helper.execute_query(query='''select * from reporting.email_activities limit 1;''')

print results
```

## Optional -> Setting up your ~/.bash_profile (Mac only)  
- If you put these variables in your bash profile then you won't need to pass them into the class every time you use it.

```Bash
export db_name='db_name'
export db_host='db_host'
export db_user='db_user'
export db_password='db_password'
export db_port='db_port'
```

- Don't forget to source your bash profile using terminal

```Bash
source ~/.bash_profile
```

- Now try it in Python
```Python
from PGHelper import PGHelper

query = '''select * from schema.table limit 1;'''

with PGHelper() as pg_helper:
    results = pg_helper.execute_query(query=query)

print results
```

When there are no values passed in, the class will attempt to grab them from the environment.

## Don't load everything into memory
- When you're working with larger datasets it's not a good idea to load all of your query results into memory.  What we can do instead is work with a named cursor.  We can do this by setting the parameter "cursor_name='anything'".  Then we can call the iter_query function and work with one record at a time.

```Python
from PGHelper import PGHelper

# Don't forget to set up your environment variables
with PGHelper(cursor_name='stream') as pg_helper:
    query = '''select * from schema.table limit 10;'''
    for record in pg_helper.iter_query(query):
        print record[0]
```

- The point of this is to save on memory so let's test that.  In this example we will load all of the results into a variable called results and look at the memory usage.  If you don't already have guppy installed you can install it using "pip install guppy" in terminal.

```Python
from PGHelper import PGHelper
from guppy import hpy
h = hpy()
start = h.heap().size

with PGHelper(cursor_name='stream') as pg_helper:
    results = pg_helper.execute_query(query='''select * from schema.table limit 10000;''')

finish = h.heap().size
print ''
print finish - start, 'bytes'
# >> 5320864 bytes
```

- Now let's use iter_query and see what the memory usage is

```Python
from PGHelper import PGHelper
from guppy import hpy
h = hpy()
start = h.heap().size

with PGHelper(cursor_name='stream') as pg_helper:
    query = '''select * from schema.table limit 10000;'''
    for record in pg_helper.iter_query(query):
        print record[0]
finish = h.heap().size
print ''
print finish - start, 'bytes'
# >> 8,000 bytes
```

Looks like it's working.  5 million to 8 thousand bytes of memory is a pretty dramatic difference.

## Postgres Helper
This class is meant to make working with Postgres a little bit easier.

#### What you need...
1. Works with Python 2.7

2. Download the files (PGHelper.py and requirements.txt)

3. Install requirements

```bash
pip install -r requirements.txt
```

#### Start using it

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

#### **Optional** -> Setting up your ~/.bash_profile (Mac only).  
- If you put these variables in your bash profile then you won't need to pass them into the class every time you use it.

```Bash
export db_name='db_name'
export db_host='db_host'
export db_user='db_user'
export db_password='db_password'
export db_port='db_port'
```

- Don't forget to source your bash profile

```Bash
source ~/.bash_profile
```

- Now try it in Python.
```Python
from PGHelper import PGHelper

query = '''select * from schema.table limit 1;'''

with PGHelper() as pg_helper:
    results = pg_helper.execute_query(query=query)

print results
```

When there are no values passed in, the class will attempt to grab them from the environment.

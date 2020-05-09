## Google DataStore Helper Class

Works with Python 3.*.  The example below gets all data from a DataStore kind/table.

```python
from DSHelper import *

config = {'project-id': 'your-project-id'}

ds = DSHelper(config)

kind = 'your-datastore-kind'
tick_ids = [ {'kind': kind, 'entity_id': a} for a in ds.getAllIds(kind=kind) ]

results = []
# can only query a max of 1000 entities from Datastore at a time
for t in range(0, len(tick_ids), 1000):
    results += ds.batchRead(tick_ids[t:t+1000])
```

- TODO: Add examples for insert, update and query

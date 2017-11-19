## S3BucketHelper

This class is meant to make working with boto3 a little easier.  I have only
  gone as far as to provide CRUD capabilities in S3 buckets.
<br /><br />
This class will work with Bluemix (IBM Cloud) S3 buckets and should work with
  AWS buckets too, although I haven't tested that yet.  

#### What you need...
1. Works with Python 2.7

2. AWS credentials

```bash
vim ~/.aws/credentials
```

```
[default]
aws_access_key_id = {Access Key ID}
aws_secret_access_key = {Secret Access Key}
```

3. install requirements

```bash
pip install -r requirements.txt
```

4. an endpoint url (Where is your bucket located?)

#### Start using it

```Python
import os
from S3BucketHelper import S3BucketHelper

endpoint = os.environ['ENDPOINT']

bh = S3BucketHelper(endpoint=endpoint)
bh.bucket_name = 'new-bucket'

bh.create_bucket()

bh.upload_object(object_name='requirements.txt', replace=True)
bh.upload_object(object_name='README.md', replace=True)

print bh.list_object_names()
# >> ['README.md', 'requirements.txt']

bh.download_object(object_name='requirements.txt', replace=True)

bh.delete_all_objects()

bh.delete_bucket()
```

#### Hope this helps :)

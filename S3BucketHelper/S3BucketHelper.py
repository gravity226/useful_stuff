class S3BucketHelper():
    import boto3
    import os
    import logging

    def __init__(self, endpoint=False, bucket_name=False):
        self.endpoint = endpoint or self.os.environ['ENDPOINT']
        self.bucket_name = bucket_name
        self.cos = self.boto3.client('s3', endpoint_url=self.endpoint)
        self.logger = self.logging.getLogger('S3BucketHelper')

    def list_bucket_names(self):
        response = self.cos.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']] if 'Buckets' in response.keys() else []

    def bucket_exists(self, bucket_name=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            return bucket_name in self.list_bucket_names()
        else:
            raise Exception ('No bucket name found...')

    def create_bucket(self, bucket_name=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                msg = 'Bucket already exists: ' + str(bucket_name)
            else:
                msg = 'Bucket created: ' + str(bucket_name)
                self.cos.create_bucket(Bucket=bucket_name)

        else:
            raise Exception ('No bucket_name found...')

        self.logger.info(msg)

    def delete_bucket(self, bucket_name=False, delete_objects=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                if len(self.list_object_names(bucket_name)) == 0 or delete_objects:
                    msg = 'Bucket deleted: ' + str(bucket_name)
                    if delete_objects:
                        self.delete_all_objects(bucket_name)
                    self.cos.delete_bucket(Bucket=bucket_name)
                else:
                    raise Exception ('You need to run the function delete_all_objects before deleting this bucket: ' + bucket_name)
            else:
                msg = 'Bucket does not exist: ' + str(bucket_name)

        else:
            raise Exception ('No bucket_name found...')

        self.logger.info(msg)

    def list_object_names(self, bucket_name=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                response = self.cos.list_objects(Bucket=bucket_name)
                return [object['Key'] for object in response['Contents']] if 'Contents' in response.keys() else []
            else:
                msg = 'Bucket does not exist: ' + str(bucket_name)
                raise Exception (msg)
        else:
            raise Exception ('No bucket_name found...')

    def object_exists(self, object_name, bucket_name=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                return object_name in self.list_object_names(bucket_name)
            else:
                msg = 'Bucket does not exist: ' + str(bucket_name)
                raise Exception (msg)
        else:
            raise Exception ('No bucket_name found...')

    def upload_object(self, local_file_name, save_name=False, bucket_name=False, replace=False):
        bucket_name = bucket_name or self.bucket_name
        save_name = save_name or local_file_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                if not self.object_exists(save_name) or replace:
                    self.cos.upload_file(Filename=local_file_name, Bucket=bucket_name, Key=save_name)
                    msg = 'Object created: ' + str(save_name)
                else:
                    msg = 'Object already exists remotely.. You need to set replace=True to replace this object.'
                    raise Exception (msg)
            else:
                msg = 'Bucket does not exist: ' + str(bucket_name)
                raise Exception (msg)
        else:
            raise Exception ('No bucket_name found...')

        self.logger.info(msg)

    def get_local_objects(self):
        return self.os.listdir('./')

    def download_object(self, object_name, save_name=False, bucket_name=False, replace=False):
        bucket_name = bucket_name or self.bucket_name
        save_name = save_name or object_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                if self.object_exists(object_name):
                    if str(save_name) not in self.get_local_objects() or replace:
                        self.cos.download_file(Key=object_name, Bucket=bucket_name, Filename=save_name)
                        msg = 'File saved locally: ' + str(save_name)
                    else:
                        msg = 'Object already exists locally.. use replace=True to replace the object: ' + str(save_name)
                        raise Exception (msg)
                else:
                    msg = 'Object does not exist: ' + str(object_name)
                    raise Exception (msg)
            else:
                msg = 'Bucket does not exist: ' + str(bucket_name)
                raise Exception (msg)
        else:
            raise Exception ('No bucket_name found...')

        self.logger.info(msg)

    def delete_object(self, object_name, bucket_name=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            if self.bucket_exists(bucket_name):
                if self.object_exists(object_name, bucket_name):
                    msg = 'Object deleted: ' + str(object_name)
                    val = self.cos.delete_object(Bucket=bucket_name, Key=object_name)
                else:
                    msg = 'Object does not exist: ' + str(object_name)
                    val = None
            else:
                msg = 'Bucket does not exist: ' + str(bucket_name)
                raise Exception (msg)
        else:
            raise Exception ('No bucket_name found...')

        self.logger.info(msg)
        return val

    def delete_all_objects(self, bucket_name=False):
        bucket_name = bucket_name or self.bucket_name

        if bucket_name:
            for object_name in self.list_object_names(bucket_name):
                self.delete_object(object_name, bucket_name)
        else:
            raise Exception ('No bucket_name found...')

        self.logger.info('There are no more objects in this bucket: ' + bucket_name)

    def delete_local_object(self, object_name):
        if str(object_name) in self.get_local_objects():
            self.os.remove(object_name)
            msg = 'Object deleted locally: ' + str(object_name)
        else:
            msg = 'Object does not exist locally: ' + str(object_name)

        self.logger.info(msg)

if __name__ == '__main__':
    import os
    import logging
    import coloredlogs

    space = logging.INFO
    coloredlogs.install(level='INFO')
    logging.basicConfig(level=space)

    endpoint = os.environ['ENDPOINT']

    bh = S3BucketHelper(endpoint=endpoint)

    bh.bucket_name = 'test-create-bucket'

    bh.create_bucket('test-create-bucket')














#

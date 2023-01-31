from dotenv import dotenv_values

from google.cloud import storage

config = dotenv_values(".env")

# User must first configure Google Cloud Credentials. See README for more details.
# Needs to be tested in current environment so will not work yet
class GCPStorage:
    def __init__(self) -> None:
        self.storage_client = storage.Client()
        self.buckets = []
        self.populate_buckets()


    def populate_buckets(self):
        buckets = self.storage_client.list_buckets()
        for bucket in buckets:
            self.buckets.append(bucket.name)

    def list_buckets(self):
        """Lists all buckets: https://cloud.google.com/storage/docs/listing-buckets#storage-list-buckets-python"""
        buckets = self.storage_client.list_buckets()
        for bucket in buckets:
            print(bucket.name)

    def make_bucket(self, bucket_name:str):
        """Makes a bucket"""
        bucket = self.storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket.name} created.")

    def view_all_buckets(self):
        for bucket in self.buckets:
            print(bucket)
            blobs = self.storage_client.list_blobs(bucket)
            for blob in blobs:
                print(blob.name)
            print()

    def view_a_bucket(self, bucket_name):
        print(f"Viewing bucket: {bucket_name}")
        blobs = self.storage_client.list_blobs(bucket_name)
        for blob in blobs:
            print(blob.name)
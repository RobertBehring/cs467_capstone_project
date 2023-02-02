import os
import random
import argparse
from dotenv import load_dotenv
#from data_maker import get_rand_ookla
from google.cloud import storage

load_dotenv()
STORAGE_BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME")

# User must first configure Google Cloud Credentials. See README for more details.
"""
Functions for interacting with GCP Cloud Storage. Creates a Storage Client and populates a list containing the names of available buckets.
Allows user to: 1) view buckets and their contents, 2) upload data to buckets 
"""
class GCPStorage:
    def __init__(self) -> None:
        self.storage_client = storage.Client()
        self.buckets = []
        self.populate_buckets()


    def populate_buckets(self):
        """
        Retrives the names of all buckets available in the storage cloud and stores them
        in a list. https://cloud.google.com/storage/docs/listing-buckets#storage-list-buckets-python
        """
        buckets = self.storage_client.list_buckets()
        for bucket in buckets:
            self.buckets.append(bucket.name)

    def print_buckets(self):
        """Prints all bucket names. """
        for bucket in self.buckets:
            print(bucket)

    def make_bucket(self, bucket_name:str):
        """Makes a bucket."""
        bucket = self.storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket.name} created.")

    def view_contents_all_buckets(self):
        """Prints contents of all buckets"""
        for bucket in self.buckets:
            print(bucket)
            blobs = self.storage_client.list_blobs(bucket)
            for blob in blobs:
                print(blob.name)
            print()

    def view_a_bucket(self, bucket_name):
        """Prints name of blobs in a given bucket."""
        print(f"Viewing bucket: {bucket_name}")
        blobs = self.storage_client.list_blobs(bucket_name)
        for blob in blobs:
            print(blob.name)

    # TODO: function for uploading json file to bucket 
    def upload_to_bucket(self, storage_bucket_name, file_path=None):
        # Create the blob's name
        dest_blob_name = os.getenv("DESTINATION_BLOB_NAME")
        file_num = str(random.randint(1000,9999))
        dest_blob_name = dest_blob_name + '_' + file_num

        # Link to desired bucket and create new blob
        bucket = self.storage_client.bucket(storage_bucket_name)
        blob = bucket.blob(dest_blob_name)

        # Know the json file path
        if file_path:
            blob.upload_from_filename(file_path)
        else:
            # Need to make the json still
            pass
#            data = get_rand_ookla()
#           print(data)


        print(f"Uploaded {dest_blob_name} to {storage_bucket_name}")

if __name__ == "__main__":
    storage = GCPStorage()
    storage.print_buckets()
    storage.view_a_bucket(STORAGE_BUCKET_NAME)
    storage.upload_to_bucket(STORAGE_BUCKET_NAME, "random_ookla_1000.json")
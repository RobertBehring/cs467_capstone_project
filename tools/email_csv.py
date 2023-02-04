from google.cloud import bigquery
from google.cloud import storage
from datetime import datetime
import io
import csv
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64

# Set your project and dataset
project_id = "cs467-capstone-dummy-data"
dataset_id = "DeviceBroadbandData"
table_id = "Multistream"
bucket_name = "bquery_csv_export"
# Get the current time
now = datetime.now()

# Format the time into a string
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
destination_file_name = timestamp + ".bq_export" + ".csv"

# Initialize a client for BigQuery
bigquery_client = bigquery.Client(project=project_id)

# Query the data you want to export
query = "SELECT * FROM `" + dataset_id + "." + table_id + "`"
query_job = bigquery_client.query(query)
results = query_job.result()

# Write the results to a CSV file
csv_file = io.StringIO()
writer = csv.writer(csv_file)

# Write header row
header = [field.name for field in results.schema]
writer.writerow(header)

# Write data rows
for row in results:
    writer.writerow(list(row.values()))

# Upload the CSV file to a bucket in GCS
gcs = storage.Client(project=project_id)
bucket = gcs.bucket(bucket_name)
blob = bucket.blob(destination_file_name)
blob.upload_from_string(csv_file.getvalue(), content_type='text/csv')


# print("Exported data to: " + "gs://" + bucket_name + "/" + destination_file_name)

message = Mail(
    from_email='riemere@oregonstate.edu',
    to_emails='erictriemer@gmail.com',
    subject='BigQuery Export',
    html_content='<strong>This is a test email with a CSV BigQuery Export</strong>')

# Encode the contents of the csv file as Base64
base64_encoded = base64.b64encode(csv_file.getvalue().encode("utf-8")).decode("utf-8")

# create attachment
attachedFile = Attachment(
    FileContent(base64_encoded),
    FileName(destination_file_name),
    FileType('text/csv'),
    Disposition('attachment')
)
message.attachment = attachedFile

# send email
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
response = sg.send(message)
print(response.status_code, response.body, response.headers)

import base64
from google.cloud import bigquery
from datetime import datetime as dt
import io
import csv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from dotenv import load_dotenv

"""
This file is a prototype version of email_csv.py. Produced to demonstrate 
the CSV report to Jim Cupples on 02/13/23. Running this program will send
a CSV report to the recipient email list hard-coded below. 

Limitations include:
- No connection to GCP authentication
  - No uploading information to cloud buckets
- Hard-coded recipient email list
  
"""

# Collect secrets from dotenv
load_dotenv()

sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
sender_email = os.getenv("SENDER_EMAIL")

def get_query():
    # Set your project and dataset
    # project_id = "cs467-capstone-dummy-data"
    dataset_id = "DeviceBroadbandData"
    table_id = "Multistream"

    # Initialize a client for BigQuery
    bigquery_client = bigquery.Client()
    
    query = "SELECT Timestamp,TestStartTime,ClientIP,ClientLat,ClientLon,DownloadValue,DownloadUnit,UploadValue,UploadUnit,Ping,PingUnit,ServerLatency,ServerLatencyUnit,Isp,IspDownloadAvg,IspUploadAvg FROM `" + dataset_id + "." + table_id + "` WHERE Timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)"
    query_job = bigquery_client.query(query)

    return query_job.result()


def send_csv_email():
    query = get_query()

    # Write the results to a CSV file
    now = dt.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    destination_file_name = timestamp + ".bq_export" + ".csv"

    csv_file = io.StringIO()
    writer = csv.writer(csv_file)

    # Write header row
    header = [field.name for field in query.schema]
    writer.writerow(header)

    # Write data rows
    for row in query:
        writer.writerow(list(row.values()))

    email_list = ["behringr@oregonstate.edu", "younjada@oregonstate.edu", "jim@allthefarms.com"]

    # Create the email message
    message = Mail(
        from_email=sender_email,
        to_emails=email_list,
        subject='BigQuery Export',
        html_content='<strong>This is a test email with a CSV BigQuery Export</strong>'
    )

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
    sg = SendGridAPIClient(sendgrid_api_key)
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)

if __name__ == '__main__':
    send_csv_email()
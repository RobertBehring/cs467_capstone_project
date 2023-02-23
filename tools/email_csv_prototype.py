import base64
from google.cloud import bigquery
import datetime as dt
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
    
    query = "SELECT TestStartTime,ClientIP,ClientLat,ClientLon,DownloadValue,DownloadUnit,UploadValue,UploadUnit,Ping,PingUnit,ServerLatency,ServerLatencyUnit,Isp,IspDownloadAvg,IspUploadAvg FROM `" + dataset_id + "." + table_id + "` WHERE Timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 20 DAY)"
    query_job = bigquery_client.query(query)

    return query_job.result()


def send_csv_email():
    query = get_query()

    # Write the results to a CSV file
    now = dt.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    destination_file_name = timestamp + ".bq_export" + ".csv"

    csv_file = io.StringIO()
    writer = csv.writer(csv_file)

    # Write header row
    header = [field.name for field in query.schema]
    writer.writerow(header)

    # Statistics
    num_records = 0
    downloads = list()
    uploads = list()
    pings = list()

    # Write data rows
    for row in query:
        writer.writerow(list(row.values()))
        num_records += 1
        downloads.append(row["DownloadValue"])
        uploads.append(row["UploadValue"])
        pings.append(row["Ping"])

    email_date_now = now.strftime("%A %B %d, %Y")
    email_date_prev = (now - dt.timedelta(days=1)).strftime("%A %B %d, %Y")
    email_list = ["behringr@oregonstate.edu", "younjada@oregonstate.edu", "riemere@oregonstate.edu"]
    email_body = f'<h1><em>Report: </em>Device Broadband Data</h1><br>'\
                 f'<strong>{email_date_prev} to {email_date_now}</strong><br>'\
                 '<table cellspacing="2" bgcolor="#000000">'\
                    '<tr bgcolor="cccccc">'\
                        '<th>Field</th>'\
                        '<th>MAX</th>'\
                        '<th>MIN</th>'\
                        '<th>AVG</th>'\
                    '</tr>'\
                    '<tr bgcolor="ffffff">'\
                        '<td>Download Value (bps)</td>'\
                        f'<td>{round(max(downloads), 3)}</td>'\
                        f'<td>{round(min(downloads), 3)}</td>'\
                        f'<td>{round(sum(downloads)/len(downloads), 3)}</td>'\
                    '</tr>'\
                    '<tr bgcolor="cccccc">'\
                        '<td>Upload Value (bps)</td>'\
                        f'<td>{round(max(uploads), 3)}</td>'\
                        f'<td>{round(min(uploads), 3)}</td>'\
                        f'<td>{round(sum(uploads)/len(uploads), 3)}</td>'\
                    '</tr>'\
                    '<tr bgcolor="ffffff">'\
                        '<td>Ping Time (ms)</td>'\
                        f'<td>{round(max(pings), 3)}</td>'\
                        f'<td>{round(min(pings), 3)}</td>'\
                        f'<td>{round(sum(pings)/len(pings), 3)}</td>'\
                    '</tr>'\
                '</table>'


    # Create the email message
    message = Mail(
        from_email=sender_email,
        to_emails=email_list,
        subject='Daily Report: Device Broadband Data',
        html_content=email_body
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
from google.cloud import bigquery
import json

client = bigquery.Client()
# Project
project_id = "cs467-capstone-dummy-data"
# Dataset (Database)
dataset_id = "DeviceBroadbandData"
# NDT-7 Table
ndt7_table_id = '.'.join([project_id, dataset_id, "NDT-7"])
ndt7_table_query_id = '`' + ndt7_table_id + '`'
ndt7_table = client.get_table(ndt7_table_id)
# Multistream Table
multistream_table_id = '.'.join([project_id, dataset_id, "Multistream"])
multistream_table_query_id = '`' + multistream_table_id + '`'
multistream_table = client.get_table(multistream_table_id)

"""CREATE"""


"""READ"""
# Query Statements
multistream_queries = {
    "selectAll": """SELECT * FROM {}\n""".format(multistream_table_query_id),
    "selectDown/Upload": """SELECT TestName, ClientIP, TestStartTime, TestEndTime, DownloadValue, DownloadUnit, UploadValue, UploadUnit FROM {}\n""".format(multistream_table_query_id)
}

"""Time Selection"""

times = {
    "daily": """WHERE TestStartTime > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)\n""",
    "weekly": """WHERE TestStartTime > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)\n""",
    "monthly": """WHERE TestStartTime > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 31 DAY)\n""",
    "yearly": """WHERE TestStartTime > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)\n"""
}

"""Functions"""
def send_query(query: str):
    query_job = client.query(query)
    return query_job.result()

def display_table_info(table):
    table_info = table.project + table.dataset_id + table.table_id
    table_schema = table.schema
    table_description = table.description
    table_rows = table.num_rows
    print("-----------------------------------------------------------")
    print("Got table {}\n".format(table_info))
    for schema in table_schema:
        print(schema)
    print()
    print("Table description: {}".format(table_description))
    print("Table has {} rows\n".format(table_rows))
    print("-----------------------------------------------------------")

def test_queries(query_dict: dict):
    limiter = "LIMIT 1"
    for query in query_dict.keys():
        print("Running Query: {}".format(query))
        for row in send_query(query_dict[query]+limiter):
            print(row)
        print("-----------------------------------------------------------")

def insert_json_uri(table, table_id: str, bucket_uri):
    job_config = bigquery.LoadJobConfig(
        schema=table.schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    
    load_job = client.load_table_from_uri(
        bucket_uri,
        table_id,
        location="us-west1",   # Must match the destination dataset location
        job_config=job_config,
    )   # Make an API request.

    try:
        load_job.result()  # Waits for the job to complete.
    except:
        print(load_job.errors)
        return

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))

if __name__ == '__main__':
    display_table_info(ndt7_table)
    bucket_uri = "gs://pagcasa-dummy-data/200-mlabRandomizedData.JSON"
    insert_json_uri(ndt7_table, ndt7_table_id, bucket_uri)
    # test_queries(read_query)
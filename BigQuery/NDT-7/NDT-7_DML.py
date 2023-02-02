from google.cloud import bigquery
import json

client = bigquery.Client()
project_id = "cs467-capstone-dummy-data"
dataset_id = "DeviceBroadbandData"
ndt7_table_id = "NDT-7"

table_id = '.'.join([project_id, dataset_id, ndt7_table_id])
table_query_id = '`' + table_id + '`'

table = client.get_table(table_id)

table_info = table.project + table.dataset_id + table.table_id
table_schema = table.schema
table_description = table.description
table_rows = table.num_rows



"""CREATE"""
# Query Statements

"""READ"""
# Query Statements
read_query = {
    "all": """SELECT *FROM {}""".format(table_query_id)
}

"""Functions"""
def send_query(query: str):
    query_job = client.query(query)
    return query_job.result()

def display_table_info():
    print("-----------------------------------------------------------")
    print("Got table {}\n".format(table_info))
    for schema in table_schema:
        print(schema)
    print()
    print("Table description: {}".format(table_description))
    print("Table has {} rows\n".format(table_rows))
    print("-----------------------------------------------------------")

def test_queries(query_dict: dict):
    limiter = "\nLIMIT 1"
    for query in query_dict.keys():
        print("Running Query: {}".format(query))
        for row in send_query(query_dict[query]+limiter):
            print(row)
        print("-----------------------------------------------------------")


if __name__ == '__main__':
    display_table_info()
    test_queries(read_query)
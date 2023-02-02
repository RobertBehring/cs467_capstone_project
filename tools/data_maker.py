"""
Title: data_maker.py
Date: 01/30/23
Author(s): Robert Behring
Description:
    data_maker.py produces a random set of ookla and mlab data given a 
    number of output data. Randomized data points are as follows:
        "TestStartTime"
        "TestEndTime"
        "DownloadValue"
        "UploadValue"
        "Ping"
        "BytesSent"
        "BytesReceived"
"""
import sys
import time
import random
import json
import textwrap

# Ookla/M-Lab JSON (Null values changed to None)
ookla = {
    "TestName": "speedtest-cli-multi-stream", 
    "TestStartTime": "2023-01-28T17:42:48.741939", 
    "TestEndTime": "2023-01-28T17:43:12.619381", 
    "MurakamiLocation": "PolkCountyDellCB", 
    "MurakamiConnectionType": "wired", 
    "MurakamiNetworkType": "-", "MurakamiDeviceID": "", 
    "DownloadValue": 32079319.23103464, 
    "DownloadUnit": "Bit/s", 
    "UploadValue": 6178827.933482051, 
    "UploadUnit": "Bit/s", 
    "Ping": 56.861, 
    "PingUnit": "ms", 
    "BytesSent": 7897088, 
    "BytesReceived": 40532993, 
    "Share": None, 
    "Timestamp": "2023-01-28T17:42:49.284868Z", 
    "ServerURL": "http://ook-sea-x1.puregig.net:8080/speedtest/upload.php", 
    "ServerLat": "47.6062", 
    "ServerLon": "-122.3321", 
    "ServerName": "Seattle, WA", 
    "ServerCountry": "United States", 
    "ServerCountryCode": "US", 
    "ServerSponsor": "Netprotect", 
    "ServerID": "37495", 
    "ServerHost": "ook-sea-x1.puregig.net:8080", 
    "ServerDistance": 2269.7755644877557, 
    "ServerLatency": 56.861, 
    "ServerLatencyUnit": "ms", 
    "ClientIP": "172.56.152.192", 
    "ClientLat": "37.751", 
    "ClientLon": "-97.822", 
    "Isp": "T-Mobile USA", 
    "IspRating": "3.7", 
    "Rating": "0", 
    "IspDownloadAvg": "0", 
    "IspUploadAvg": "0", 
    "LoggedIn": "0", 
    "Country": "US"
}
mlab = {
    "TestName": "ndt7", 
    "TestStartTime": "2023-01-28T17:42:23.968459", 
    "TestEndTime": "2023-01-28T17:42:48.231296", 
    "MurakamiLocation": "PolkCountyDellCB", 
    "MurakamiConnectionType": "wired", 
    "MurakamiNetworkType": "-", 
    "MurakamiDeviceID": "", 
    "ServerName": "ndt-mlab2-sea02.mlab-oti.measurement-lab.org", 
    "ServerIP": "2001:5a0:4400::24", 
    "ClientIP": "2607:fb90:3313:bfe3:eab5:d0ff:fecf:78cd", 
    "DownloadUUID": "ndt-vh8kh_1673479228_0000000000100115", 
    "DownloadValue": 25.4786339719012, 
    "DownloadUnit": "Mbit/s", 
    "DownloadError": None, 
    "UploadValue": 5.65328875730213, 
    "UploadUnit": "Mbit/s", 
    "UploadError": None, 
    "DownloadRetransValue": 0, 
    "DownloadRetransUnit": "%", 
    "MinRTTValue": 90.031, 
    "MinRTTUnit": "ms"
}

# System Messages
exit_msg = "\nProgram exiting. . .\n"
value_err = "\nERROR: Incompatible Value"
usage = "\nusage: python data_maker.py NUM\n"
help_msg = "help message"

# randomization variables
random.seed(time.localtime().tm_hour + time.localtime().tm_min + time.localtime().tm_sec)

# output variables
print_to_stdout = False
num_ookla = 0
num_mlab = 0
keys_in_common = [x for x in ookla.keys() if x in mlab]

# functions
def get_current_time() -> str:
    local_time = time.localtime()
    year = local_time.tm_year
    month = local_time.tm_mon
    day = local_time.tm_mday
    hour = local_time.tm_hour
    minute = local_time.tm_min
    second = local_time.tm_sec

    return f"{year}-{month}-{day}T{hour}:{minute}:{second}"

def get_rand_bit_per_sec() -> float:
    return random.randrange(0, 9999999) + random.random()

def get_rand_ping_time() -> float:
    return round(random.randrange(0, 200) + random.random(), 3)

def get_rand_bytes() -> int:
    return random.randrange(0, 9999999)

def get_rand_dist() -> float:
    return random.randrange(0, 9999) + random.random()

def get_rand_data(type: str) -> dict:
    if type == "ookla":
        rand_data = ookla.copy()
        rand_data["Ping"] = get_rand_ping_time()
        rand_data["BytesSent"] = get_rand_bytes()
        rand_data["BytesReceived"] = get_rand_bytes()
    if type == "mlab":
        rand_data = mlab.copy()
        rand_data["MinRTTValue"] = get_rand_ping_time()
    rand_data["TestStartTime"] = get_current_time()
    rand_data["DownloadValue"] = get_rand_bit_per_sec()
    rand_data["UploadValue"] = get_rand_bit_per_sec()
    rand_data["TestEndTime"] = get_current_time()

    return rand_data

def set_print():
    global print_to_stdout 
    print_to_stdout = True

def set_num_ookla(num: int):
    global num_ookla
    num_ookla = num

def set_num_mlab(num: int):
    global num_mlab
    num_mlab = num

def display_help():
    print(help_msg)

def write_to_json(file_name: str, data: dict):
    f = open(file_name, "w")
    f.write(data)
    f.close()

def gen_data(num: int, mlab=False):
    for i in range(num):
        if mlab:
            rand_data = json.dumps(get_rand_data("mlab"))
            file_name = str(i+1) + "-mlabRandomizedData.JSON"
        else:
            rand_data = json.dumps(get_rand_data("ookla"))
            file_name = str(i+1) + "-ooklaRandomizedData.JSON"
        if print_to_stdout:
            print(file_name)
            print()
            wrapper = textwrap.TextWrapper(width=80)
            rand_data = wrapper.fill(text=rand_data)
            print(rand_data)
            print()
        else:
            write_to_json(file_name, rand_data)
        
# Input
msg_funcs = {
    "-p": set_print,
    "-h": display_help
}
output_funcs = {
    "-ookla": set_num_ookla,
    "-mlab": set_num_mlab
}
for i in range(1, len(sys.argv)):
    if sys.argv[i] in msg_funcs:
        msg_funcs[sys.argv[i]]()
    if sys.argv[i] in output_funcs:
        try:
            output_funcs[sys.argv[i]](int(sys.argv[i+1]))
        except:
            print("\n\t\t\t\t>>>>>> ERROR <<<<<<")
            print(usage)
            print(f"       Please provide an integer for the number of {sys.argv[i][1:]} data you would like to output\n")
            print("\n\t\t\t\tProgram Exiting. . .\n\n")
            sys.exit(1)


if __name__ == '__main__':
    print("\t\t===========\tGENERATING DATA\t===========\n\n")
    gen_data(num_ookla)
    gen_data(num_mlab, mlab=True)
    print("\n\t\t\t\tProgram Exiting. . .\n\n")

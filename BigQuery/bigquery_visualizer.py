import DeviceBroadbandData_DML as dml
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

bigquery_data = dml.send_query(dml.multistream_queries["requested"])

timestamps = list()
download_values = list()
upload_values = list()
pings = list()
server_latencies = list()


for row in bigquery_data:
    if row["Timestamp"] not in timestamps:
        timestamps.append(row["Timestamp"])
        download_values.append(row["DownloadValue"]/1000)
        upload_values.append(row["UploadValue"]/1000)
        pings.append(row["Ping"])
        server_latencies.append(row["ServerLatency"])
        download_unit = row["DownloadUnit"]

timestamps = np.array(timestamps)

# print(timestamps)

plt.subplot(131)
plt.plot(timestamps, download_values, label="Download", color="red", linewidth=2)
plt.plot(timestamps, upload_values, label="Upload", color="blue", linewidth=2)
plt.axis([timestamps[0], timestamps[-1], min(download_values), max(download_values)])
plt.xlabel("Time")
plt.ylabel("Download Values {}".format(download_unit))
plt.title("Download/Upload vs. Time")
plt.legend()
plt.subplot(132)
plt.plot(timestamps, pings)
plt.axis([timestamps[0], timestamps[-1], min(pings), max(pings)])
plt.xlabel("Time")
plt.ylabel("Ping ms")
plt.subplot(133)
plt.plot(timestamps, server_latencies)
plt.axis([timestamps[0], timestamps[-1], min(server_latencies), max(server_latencies)])
plt.xlabel("Time")
plt.ylabel("server latency ms")

plt.show()

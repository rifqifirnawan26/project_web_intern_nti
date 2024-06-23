import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt
import numpy as np
import time
from secrets_1 import INFLUX_TOKEN

# Konfigurasi koneksi InfluxDB
token = INFLUX_TOKEN
org = "interntt"
url = "http://192.168.9.16:8086"
bucket = "intern"

# Koneksi ke InfluxDB
client = InfluxDBClient(url=url, token=token)
query_api = client.query_api()

# Fungsi untuk mengambil dan memproses data dari InfluxDB
def get_data():
    query = f'from(bucket: "{bucket}") \
              |> range(start: -10m) \
              |> filter(fn: (r) => r._measurement == "memory") \
              |> last()'
    tables = query_api.query(query, org=org)
    data = {}
    for table in tables:
        for record in table.records:
            data[record.get_field()] = record.get_value()
    return data

# Fungsi untuk memperbarui dan menampilkan grafik secara real-time
def update_plot(data):
    plt.clf()
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
    labels, values = zip(*sorted_data)
    plt.bar(labels, values)
    plt.xlabel('Tags')
    plt.ylabel('Memory Field Value')
    plt.title('Top 10 Memory Field Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.pause(1)  # Update setiap 1 detik

# Loop utama untuk memperbarui grafik secara real-time
data = {}
while True:
    new_data = get_data()
    if new_data != data:  # Hanya memperbarui jika ada perubahan data
        data = new_data
        update_plot(data)
    time.sleep(1)  # Update setiap 1 detik

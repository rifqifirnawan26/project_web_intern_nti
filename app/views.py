import io
from django.http import JsonResponse
from django.shortcuts import render
from influxdb_client import InfluxDBClient

# URL, token, dan nama bucket untuk koneksi ke InfluxDB
url = "http://192.168.9.16:8086"
token = "V2JRMGtkEm6BuyXq6QIsjdgfTysg0OY-Zc2zM3v_P0OehjwQ_cmziiSwq8rP590I14yY6ktbxMcVDTirDpuoaw=="
org = "interntt"
bucket = "intern"

def get_latest_data(time_range='1h'):
    if time_range == 'now':
        time_range = '1m'  # Set a small time range for 'now' to get the latest data

    with InfluxDBClient(url=url, token=token, org=org, timeout=20_000) as client:
        query = f"""
            option v = {{timeRangeStart: -{time_range}, timeRangeStop: now()}}

            from(bucket: "intern")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "system")
            |> filter(fn: (r) => r["_field"] == "cpu")
        """

        tables = client.query_api().query(query, org=org)

        data = {}
        for table in tables:
            for record in table.records:
                host = record["host"]
                vmid = record["vmid"]
                field_value = record.get_value()
                timestamp = record.get_time()

                key = f"{host}_{vmid}"
                if key not in data:
                    data[key] = []

                data[key].append({'field_value': field_value, 'timestamp': timestamp, 'host': host})

        return data

def get_latest_memory_data(time_range='1h'):
    if time_range == 'now':
        time_range = '1m'  # Set a small time range for 'now' to get the latest data

    with InfluxDBClient(url=url, token=token, org=org, timeout=20_000) as client:
        query = f"""
            option v = {{timeRangeStart: -{time_range}, timeRangeStop: now()}}

            from(bucket: "intern")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "system")
            |> filter(fn: (r) => r["_field"] == "mem")
            |> filter(fn: (r) => r["nodename"] == "pve")
            |> filter(fn: (r) => r["object"] == "qemu")
        """

        tables = client.query_api().query(query, org=org)

        data = {}
        for table in tables:
            for record in table.records:
                host = record["host"]
                vmid = record["vmid"]
                field_value = record.get_value()
                timestamp = record.get_time()

                key = f"{host}_{vmid}"
                if key not in data:
                    data[key] = []

                data[key].append({'field_value': field_value, 'timestamp': timestamp, 'host': host})

        return data
    
def get_latest_data2(time_range='1h'):
    with InfluxDBClient(url=url, token=token, org=org, timeout=20_000) as client:
        query = f"""
            from(bucket: "{bucket}")
            |> range(start: -{time_range})
            |> filter(fn: (r) => r["_measurement"] == "system")
            |> filter(fn: (r) => r["_field"] == "cpu")
        """
        tables = client.query_api().query(query, org=org)
        records = []

        for table in tables:
            for record in table.records:
                records.append({
                    'host': record['host'],
                    'value': record.get_value(),
                    'timestamp': record.get_time()
                })

        return records
    
def get_cpu_metrics(time_range='1h'):
   with InfluxDBClient(url=url, token=token, org=org, timeout=20_000) as client:
        query = f"""
            from(bucket: "{bucket}")
            |> range(start: -{time_range})
            |> filter(fn: (r) => r["_measurement"] == "system")
            |> filter(fn: (r) => r["_field"] == "cpu")
        """
        tables = client.query_api().query(query, org=org)
        records = []

        for table in tables:
            for record in table.records:
                records.append({
                    'host': record['host'],
                    'value': record.get_value(),
                    'timestamp': record.get_time().isoformat(),
                })

        return records
   
def get_disk_read(time_range='1h'):
    with InfluxDBClient(url=url, token=token, org=org, timeout=20_000) as client:
        query = f"""
            from(bucket: "intern")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "system")
            |> filter(fn: (r) => r["_field"] == "diskread")
        """

        tables = client.query_api().query(query, org=org)
        records = []

        for table in tables:
            for record in table.records:
                records.append({
                    'host': record['host'],
                    'value': record.get_value(),
                    'timestamp': record.get_time().isoformat(),
                })

        return records



def calculate_percentage(data):
    percentages = {}
    for key, records in data.items():
        total_value = sum(record['field_value'] for record in records)
        total_records = len(records)
        
        if total_records == 0:
            percentages[key] = {"percentage": 0, "host": records[0]['host'], "timestamp": records[0]['timestamp']}
        else:
            percentages[key] = {
                "percentage": (total_value / total_records) * 100,
                "host": records[0]['host'],
                "timestamp": records[0]['timestamp']
            }
    return percentages


def calculate_percentage2(data):
    percentages = {}
    for key, records in data.items():
        total_value = sum(record['field_value'] for record in records)
        total_records = len(records)
        
        if total_records == 0:
            percentages[key] = {"percentage": 0, "host": records[0]['host']}
        else:
            percentages[key] = {
                "percentage": (total_value / total_records) / 1000000000,
                "host": records[0]['host']
            }
    return percentages

def calculate_percentage3(data):
    host_data = {}
    for record in data:
        host = record['host']
        if host not in host_data:
            host_data[host] = {'total_value': 0, 'total_records': 0}
        host_data[host]['total_value'] += record['value']
        host_data[host]['total_records'] += 1

    host_percentages = {host: (data['total_value'] / data['total_records']) * 100 for host, data in host_data.items()}
    return host_percentages

def calculate_percentage4(data):
    percentages = {}
    for key, records in data.items():
        total_value = sum(record['field_value'] for record in records)
        total_records = len(records)
        
        if total_records == 0:
            percentages[key] = {"percentage": 0, "host": records[0]['host'], "timestamp": records[0]['timestamp']}
        else:
            percentages[key] = {
                "percentage": (total_value / total_records) * 100,
                "host": records[0]['host'],
                "timestamp": records[0]['timestamp']
            }
    return percentages

def get_metrics(request):
    time_range = request.GET.get('time_range', '1h')
    data = get_latest_data(time_range)
    percentages = calculate_percentage(data)
    return JsonResponse(percentages, safe=False)

def get_memory_metrics(request):
    time_range = request.GET.get('time_range', '1h')
    data = get_latest_memory_data(time_range)
    percentages = calculate_percentage2(data)
    return JsonResponse(percentages, safe=False)

def get_metrics3(request):
    time_range = request.GET.get('time_range', '1h')
    data = get_latest_data2(time_range)
    percentages = calculate_percentage3(data)

    active_hosts = 0
    high_utilization_hosts = 0
    total_utilization = 0
    total_hosts = len(percentages)
    
    host_details = []

    for host, percentage in percentages.items():
        total_utilization += percentage
        if percentage > 0:
            active_hosts += 1
            if percentage > 85:
                high_utilization_hosts += 1
        
        host_details.append({
            'host_name': host,
            'cpu_utilization': percentage,
            'ip_address': '192.168.1.1'  # Replace with actual IP address if available
        })
    
    inactive_hosts = total_hosts - active_hosts
    average_utilization = total_utilization / total_hosts if total_hosts > 0 else 0

    result = {
        'summary': {
            'total_hosts': total_hosts,
            'active_hosts': active_hosts,
            'inactive_hosts': inactive_hosts,
            'average_utilization': average_utilization,
            'high_utilization_hosts': high_utilization_hosts
        },
        'details': host_details
    }

    return JsonResponse(result, safe=False)

def get_disk1(request):
    time_range = request.GET.get('time_range', '1h')
    data = get_disk_read(time_range)
    percentages = calculate_percentage4(data)
    return JsonResponse(percentages, safe=False)

def dashboard(request, time_range='1h'):
    data = get_latest_data(time_range)
    percentages = calculate_percentage(data)
    return render(request, 'dashboard.html', {'data': percentages, 'time_range': time_range})

def dashboard(request, time_range='1h'):
    data = get_latest_memory_data(time_range)
    percentages = calculate_percentage2(data)
    return render(request, 'dashboard.html', {'data': percentages, 'time_range': time_range})

def dashboard(request, time_range='1h'):
    data = get_disk_read(time_range)
    percentages = calculate_percentage4(data)
    return render(request, 'dashboard.html', {'data': percentages, 'time_range': time_range})

def dashboard(request):
    return render(request, 'dashboard.html')

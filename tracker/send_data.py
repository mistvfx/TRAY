import datetime
import json
import requests
import psutil

start = 0
current_window, current_process, process_info = '', '', ''

SERVER = ''
TOKEN = ""

def calculate_overall_time(window_name, process_details, stop):
    global start
    if start == 0 or process_details == 0:
        return
    data = {
            "window": window_name,
            "process_name": process_details['name'],
            "process_id": int(process_details['pid']),
            "date": start.strftime("%Y-%m-%d"),
            "start_time": start.strftime('%I:%M:%S'),
            "end_time": stop.strftime('%I:%M:%S'),
            "total_time": str(stop-start),
            "user": psutil.users()[0].name
    }

    # print(data)
    url = f'{SERVER}/hrm/api/system-tracking/'
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Token {TOKEN}'}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())

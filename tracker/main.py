from win32gui import *
import psutil
from win32process import GetWindowThreadProcessId
import threading
import datetime
import os
import time
import logging
import tempfile

# logging.basicConfig(filename=f'{tempfile.gettempdir()}{os.sep}tracker_log.log', level=logging.DEBUG)

from . import send_data

old_hwnd = None
idle_time_elapsed = 0

important_process = ['3DE4.exe', 'maya.exe', 'Silhouette.exe', 'Nuke11.3.exe', 'Nuke10.5.exe', 'meshlab.exe', 'rv.exe', 'xnview.exe', 'xnview.exe *32', 'pdplayer.exe', 'pdplayer.exe *32', 'boujou.exe', 'mochapro.exe']


def check_active_process():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        if proc.info['name'] in important_process:
            # print(proc.info)
            return True
    # print("WIP")


def timer():#
    global idle_time_elapsed
    while idle_time_elapsed != 12:
        time.sleep(60)
        idle_time_elapsed += 1
    if idle_time_elapsed == 12:
        if check_active_process():
            idle_time_elapsed = 0
            timer()
        # import win32api
        # win32api.SetSystemPowerState(True, True)
        # os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    

def get_threadname(HWND):
    pprocess = GetWindowThreadProcessId(HWND)
    try:
      p = psutil.Process(pprocess[1])
    except Exception as e:
      return 0
    #print(p.name())
    return p.as_dict(attrs=['pid', 'name'])


def main_loop():
    global old_hwnd, idle_time_elapsed
    while True:
        time.sleep(1)
        active_window = GetForegroundWindow()
        if old_hwnd != active_window:
            send_data.calculate_overall_time(GetWindowText(old_hwnd), get_threadname(old_hwnd), datetime.datetime.now())
            send_data.start = datetime.datetime.now()
            old_hwnd = active_window
            idle_time_elapsed = 0
        else:
            continue
        # process_name = get_threadname(active_window)
        # window_name = GetWindowText(GetForegroundWindow())
        # print(window_name)


def send_pc_info():
    from . import sysinfo

    data = {
        'host_name': sysinfo.host_name(),
        'ip_address': sysinfo.ip_address(),
        'mac_address': sysinfo.mac_address(),
        'user': sysinfo.user(),
        'ram': sysinfo.total_ram(),
        'processor': sysinfo.processor(),
        'processor_cores': sysinfo.processor_core(),
        'gpu': sysinfo.gpu_card(),
        'gpu_memory': sysinfo.gpu_memory()
    }


def resource_path(relative_path):
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_token():
    import json
    import tempfile
    import configparser
    import requests

    main_config = configparser.ConfigParser()
    main_details = configparser.ConfigParser()
    main_config.read(resource_path('main_config.ini'))

    send_data.SERVER = main_config.get('server', 'url')

    details_config = resource_path(f"{tempfile.gettempdir()}{os.sep}main_details.ini")
    try:
        main_details.read(details_config)
        send_data.TOKEN = main_details.get('server', 'token')
    except Exception as e:
        print(e)
        response = requests.post(f"{send_data.SERVER}/api-token-auth/", params={'username': psutil.users()[0].name}).json()
        main_details['server'] = {}
        main_details['server']['token'] = send_data.TOKEN = response['token']
        with open(details_config, 'w+') as out_file:
            main_details.write(out_file)


def start_tracker(*args):
    logging.debug("STARTING TRACKER ....")
    get_token()
    logging.debug("Token received")
    # send_pc_info()
    thread1 = threading.Thread(target=timer, args=())
    thread2 = threading.Thread(target=main_loop, args=())
    thread1.start()
    thread2.start()

    logging.debug("Tracker Threads Started")

    thread2.join()

# if __name__ == '__main__':
#     send_pc_info()
#     thread1 = threading.Thread(target=timer, args=())
#     thread2 = threading.Thread(target=main_loop, args=())
#     thread1.start()
#     thread2.start()

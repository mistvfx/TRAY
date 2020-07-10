from pystray import Menu, MenuItem, Icon
from PIL import Image

from multiprocessing import Process, freeze_support

import json
import tempfile
import requests
import sys
import os
import configparser
import logging
import atexit
import subprocess

logging.basicConfig(filename=f'{tempfile.gettempdir()}{os.sep}tray_log.log', level=logging.DEBUG)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


config = configparser.ConfigParser()
config.read(resource_path('main_config.ini'))


def on_launch_app(icon, item):
    print("LAUNCHING APP FROM : ", config.get('path', f'app_{sys.platform}'))
    subprocess.Popen(config.get('path', f'app_{sys.platform}'))



icon = Icon(
        'Mist ERP',
        Image.open(resource_path(f'assets{os.sep}icons{os.sep}favicon.ico')),
        menu=Menu(
            MenuItem(
                "Launch APP",
                on_launch_app,
                default=True,
                enabled=True,
                visible=True
            )
        )
    )


def run_systray_app():
    logging.debug('initialize icon')
    global icon
    icon.run()


@atexit.register
def stop_app_process():
    global p1, p2
    p1.terminate()
    p1.join()
    p2.terminate()
    p2.join()
    global icon
    icon.stop()
    logging.info("Terminated processes")


def send_pc_info():
    main_details = configparser.ConfigParser()
    main_details.read(resource_path(f"{tempfile.gettempdir()}{os.sep}main_details.ini"))
    import requests
    from tracker import sysinfo
    data = {
        'user': sysinfo.username(),
        'ip_address': sysinfo.ip_address()
    }
    response = requests.put(
        f"{config.get('server', 'url')}/inventory/api/computer/",
        data=data,
        headers={'Authorization': f'Token {main_details.get("server", "token")}'}
    )
    print(response.text)
    # IF CANNOT PUT - OBJECT DOES NOT EXIST
    # THEN POST TO CREATE OBJECT FOR USER
    if response.status_code == 500:
        post_resp = requests.post(
            f"{config.get('server', 'url')}/inventory/api/computer/",
            data=data,
            headers={'Authorization': f'Token {main_details.get("server", "token")}'}
        )

if __name__ == '__main__':
    send_pc_info()
    freeze_support()

    from server.main import start_app
    from tracker.main import start_tracker
    # START SYSTEM FLASK SERVER
    p1 = Process(target=start_app)
    logging.debug('Flask App init')
    p2 = Process(target=start_tracker)
    logging.debug('Tracker App init')

    p1.start()
    logging.debug('Flask App start')
    p2.start()
    logging.debug('Tracker App start')
    run_systray_app()
    logging.debug('Tray App start')
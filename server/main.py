from flask import Flask, request

from waitress import serve

from plyer import notification
import logging
import tempfile
import os
import sys

# logging.basicConfig(filename=f'{tempfile.gettempdir()}{os.sep}server_log.log', level=logging.DEBUG)

app = Flask(__name__)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


@app.route('/notify/', methods=['GET', 'POST'])
def hello():
    notification.notify(
        title="MIST ERP",
        message=request.args.get('message'),
        timeout=10,
        app_icon=resource_path(f'assets{os.sep}icons{os.sep}favicon.ico')
    )
    return 'notified'


def start_app():
    logging.debug("Starting Flask app...")
    # app.run(host='0.0.0.0', port=5000, debug=False)
    serve(app=app, host='0.0.0.0', port=5000)

#-coding:utf-8


import os
import sys
import json
import logging

curdir = os.path.dirname(os.path.realpath(__file__))
sys_path = [ ]
sys_path.append(os.path.join(curdir, "site-packages"))
for p in sys_path:
    sys.path.insert(0,p)

from flask import Flask, render_template
from config import load_config
from sunshine import Sunshine


logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    #filename=".log",
    )

def run_application(app):
    app.run(host="0.0.0.0", port=8001, threaded=True, debug=False)

def run_wsgi(app):
    from flup.server.fcgi import WSGIServer
    WSGIServer(app, bindAddress=('0.0.0.0', 8001), debug=True, multithreaded=True).run()

def sunshine_test():
    plugin_dir = os.path.join(curdir, "plugin")
    app = Flask(__name__)
    sunshine = Sunshine(app, plugin_dir)
    run_application(app)

def sunshine_wsgi():
    plugin_dir = os.path.join(curdir, "plugin")
    app = Flask(__name__)
    app.config.from_object(load_config())
    sunshine = Sunshine(app, plugin_dir)
    run_wsgi(app)

def run():
    mode = os.environ.get('MODE')
    if mode:
        sunshine_test()
    else:
        sunshine_wsgi()



if __name__ == "__main__":
    run()


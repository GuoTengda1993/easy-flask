#!/usr/bin/env python3
"""gunicorn config

"""
import os

from conf import app_conf


worker_class = app_conf.worker_class
if 'gevent' in worker_class:
    from gevent import monkey
    monkey.patch_all()

preload_app = True
daemon = True
loglevel = app_conf.loglevel
debug = False if loglevel != 'debug' else True
bind = '{}:{}'.format(app_conf.host, app_conf.port)
workers = app_conf.workers
threads = app_conf.threads

x_forwarded_for_header = 'X-FORWARDED-FOR'
path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]
pidfile = '%s/logs/gunicorn.pid' % path_of_current_dir
errorlog = '%s/logs/info.log' % path_of_current_dir
accesslog = '%s/logs/access.log' % path_of_current_dir

#!/usr/bin/env python3
"""init app

"""
from importlib import import_module
import inspect
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import List
from uuid import uuid4


from flask import Flask, g, json
# MethodViewType is removed in flask 2.x
try:
    from flask.views import MethodViewType as MethodView
except ImportError:
    from flask.views import MethodView
from werkzeug.exceptions import HTTPException

from conf import app_config


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
api_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """project config
    
    """
    SECRET_KEY = app_config.sk


def create_app():
    """create flask app

    :return:
    """
    app = Flask('easy-flask')
    app.config.from_object(BaseConfig)

    register_logging(app)
    register_apis(app)

    @app.before_request
    def setup():
        """set different log_id for each request

        :return:
        """
        g.log_id = uuid4().hex
        g.logger = logging.LoggerAdapter(app.logger, extra={'log_id': g.log_id})

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "errno": e.code,
            "msg": "[%s] %s" % (e.name, e.description),
            "log_id": g.log_id
        })
        response.content_type = "application/json"
        return response

    return app


def register_logging(app: Flask):
    logging.logThreads = 0
    logging.logProcesses = 0
    logging.logMultiprocessing = 0
    formatter = logging.Formatter('%(asctime)s [%(module)s] %(levelname)s log_id[%(log_id)s] %(message)s')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    log_level = logging.DEBUG if app.debug else logging.INFO
    file_handler.setLevel(log_level)
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    
    
def add_resource(app: Flask, resource: MethodView, urls: List[str]):
    for url in urls:
        name = resource.__name__.lower() + url.replace('/', '_')
        app.add_url_rule(url, view_func=resource.as_view(name))


def register_apis(app: Flask):
    """register api from files from api dir

    :param api:
    :return:
    """
    api_file_data = os.walk(api_dir)
    for r, _, files in api_file_data:
        imp_path_list = r.replace(basedir, '')[1:].split(os.path.sep)
        imp_path = '.'.join(imp_path_list)
        for f in files:
            if f.endswith('api.py'):
                name = f.replace('.py', '')
                imp_file = '{}.{}'.format(imp_path, name)
                module = import_module(imp_file)
                class_list = inspect.getmembers(module, inspect.isclass)
                for c in class_list:
                    if type(c[1] == MethodView) and c[0] != 'Resource':
                        add_resource(app, c[1], c[1].uri)

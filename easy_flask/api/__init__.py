#!/usr/bin/env python3
"""init app

"""
import logging
import os
from logging.handlers import RotatingFileHandler
from uuid import uuid4
from importlib import import_module
import inspect

from flask import Flask, g
from flask.views import MethodView
from flask_restful import Api


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
api_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """project config

    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'easy-flask-demo')


def create_app():
    """create flask app

    :return:
    """
    app = Flask('easy-flask')
    app.config.from_object(BaseConfig)
    api = Api(app)

    register_logging(app)
    register_apis(api)

    @app.before_request
    def setup():
        """set different log_id for each request

        :return:
        """
        g.log_id = uuid4().hex
        g.logger = logging.LoggerAdapter(app.logger, extra={'log_id': g.log_id})

    return app


def register_logging(app):
    """

    :param app:
    :return:
    """
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


def register_apis(api):
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
                        api.add_resource(c[1], *c[1].uri)

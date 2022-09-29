#!/usr/bin/env python3
"""load conf

"""
import configparser
import os
import multiprocessing


conf_dir = os.path.abspath(os.path.dirname(__file__))
conf_file = os.path.join(conf_dir, 'config.ini')


class BaseConfig(object):

    def __init__(self, section: str):
        self._section = section

    def _load_conf(self):
        config = configparser.ConfigParser()
        config.read(conf_file, encoding='utf-8')

        for k, v in config.items(self._section):
            if hasattr(self, k):
                default_val = getattr(self, k)
                try:
                    if isinstance(default_val, int):
                        v = int(v)
                    elif isinstance(default_val, float):
                        v = float(v)
                    elif isinstance(default_val, bool):
                        v = True if str(v).lower() == 'true' else False
                except ValueError:
                    v = default_val
            setattr(self, k, v)
        return


class AppConfig(BaseConfig):

    def __init__(self):
        super().__init__(section='app')
        self.host = '0.0.0.0'
        self.port = 8000
        self.workers = multiprocessing.cpu_count() * 2 + 1
        self.threads = 2
        self.loglevel = 'info'
        self.worker_class = 'tornado'
        self.timeout = 60
        self._load_conf()


app_conf = AppConfig()

#!/usr/bin/env python3
"""load conf

"""
import configparser
import os
import multiprocessing


conf_dir = os.path.abspath(os.path.dirname(__file__))
conf_file = os.path.join(conf_dir, 'config.ini')


class AppConfig:

    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8000
        self.workers = multiprocessing.cpu_count() * 2 + 1
        self.threads = 2
        self.loglevel = 'info'
        self.worker_class = 'tornado'
        self.timeout = 60
        self._load_conf()

    def _load_conf(self):
        config = configparser.ConfigParser()
        config.read(conf_file, encoding='utf-8')

        for k, v in config.items('app'):
            if k in ['port', 'workers', 'threads', 'timeout']:
                v = int(v)
            setattr(self, k, v)
        return

#!/usr/bin/env python3
"""load app

"""
import os

from api import create_app


if not os.path.exists('logs'):
    os.mkdir('logs')


app = create_app()


if __name__ == '__main__':
    from conf import AppConfig
    app_conf = AppConfig()
    app.run(host=app_conf.host, port=app_conf.port, debug=True, threaded=True)

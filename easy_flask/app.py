#!/usr/bin/env python3
"""load app

"""
import os

from api import create_app


if not os.path.exists('logs'):
    os.mkdir('logs')


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

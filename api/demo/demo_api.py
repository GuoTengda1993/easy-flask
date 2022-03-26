#!/usr/bin/env python3
"""demo api

"""
from flask import g

from internal import Resource


class DemoApi(Resource):

    uri = ['/api/demo']

    def get(self):
        req_p = {
            'num': {'type': int, 'min': 10, 'max': 100},
            'print': {'type': str, 'required': True},
            'default': {'type': str, 'default': 'demo'}
        }

        data, err = self.parse_request_data(req_pattern=req_p)
        if err:
            g.logger.warning(err)
            return err
        g.logger.info('success')
        return {'result': data}

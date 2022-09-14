#!/usr/bin/env python3
"""demo api

"""
from flask import g

from internal import Resource
from utils.parser import Type, Required, Default, Min, Max


class DemoApi(Resource):

    uri = ['/api/demo']

    def get(self):
        pattern = {
            'num': {Type: int, Min: 10, Max: 100},
            'print': {Type: str, Required: True},
            'default': {Type: str, Default: 'demo'}
        }

        data, err = self.parse_request_data(pattern=pattern)
        if err:
            g.logger.warning(err)
            return err
        g.logger.info('success')
        return {'result': data}

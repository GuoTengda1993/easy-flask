#!/usr/bin/env python3
"""define error info here

"""


class BaseError(object):
    errno = 1
    code = 500
    error_info = 'error:'

    def __init__(self, msg: str = ''):
        self.msg = self.error_info + msg


class InternalServerError(BaseError):
    errno = 1
    code = 500
    error_info = 'internal server error:'


class ParamsError(BaseError):
    errno = 2
    code = 240
    error_info = 'params error:'

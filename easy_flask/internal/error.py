#!/usr/bin/env python3
"""define error info here

"""


class BaseError(object):
    errno = 1
    code = 500
    error_info = 'error'

    def __init__(self, msg: str = ''):
        msg = self.error_info + ':' + msg if msg else self.error_info
        self.msg = msg

    def __str__(self):
        return self.msg


class InternalServerError(BaseError):
    errno = 1
    code = 500
    error_info = 'internal server error'


class ParamsError(BaseError):
    errno = 2
    code = 240
    error_info = 'params error'

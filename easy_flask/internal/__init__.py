#!/usr/bin/env python3
"""internal class and functions

"""
import json
from typing import Mapping, Union

from flask import g, request, Response
from flask.views import MethodView
from werkzeug.wrappers import Response as ResponseBase

from internal.error import BaseError
from utils.parser import parser


def unpack(value):
    """Return a two tuple of data and code"""
    if isinstance(value, BaseError):
        data = {
            'errno': value.errno,
            'msg': value.msg,
            'log_id': g.log_id
        }
        return data, value.code

    res = value
    code = 200
    msg = 'success'
    if isinstance(value, tuple):
        if len(value) == 2:
            res, code = value
        else:
            res, code, msg = value[0], value[1], value[2]

    data = {
        'errno': 0,
        'data': res,
        'msg': msg,
        'log_id': g.log_id
    }
    return data, code


class Resource(MethodView):
    """
    Represents an abstract RESTful resource. Concrete resources should
    extend from this class and expose methods for each supported HTTP
    method. If a resource is invoked with an unsupported HTTP method,
    the API will return a response with status 405 Method Not Allowed.
    Otherwise the appropriate method is called and passed all arguments
    from the url rule used when adding the resource to an Api instance. See
    :meth:`~flask_restful.Api.add_resource` for details.
    """
    representations = None
    method_decorators = []

    def dispatch_request(self, *args, **kwargs):
        # Token from flask-restful
        # change point: set log_id for each json response
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        if isinstance(self.method_decorators, Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        data, code = unpack(resp)
        res = json.dumps(data, ensure_ascii=False)
        return Response(res, status=code, content_type='application/json')

    def parse_request_data(self, pattern: Union[dict, None] = None, remove_redundant: bool = False):
        """get and parse request data

        :param pattern: use to define attrs of each params
        :param remove_redundant: remove keys in data but not in pattern
        :return:
        """
        data = dict()
        args = request.args.to_dict()
        if args:
            data.update(args)
        if request.content_type:
            if 'form' in request.content_type:
                form = request.form.to_dict()
                if form:
                    data.update(form)
            elif 'json' in request.content_type:
                body = request.json
                if body:
                    data.update(body)

        if pattern:
            data, err = parser(data=data, pattern=pattern, remove_redundant=remove_redundant)
            if err:
                return None, error.ParamsError(err)

        return data, None

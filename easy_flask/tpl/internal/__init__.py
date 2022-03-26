#!/usr/bin/env python3
"""internal class and functions

"""
import json
from typing import Mapping, Union

from flask import g, request, Response
from flask.views import MethodView
from werkzeug.wrappers import Response as ResponseBase

from internal.error import BaseError
from internal import utils


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

    def parse_request_data(self, req_pattern: Union[dict, None] = None):
        """get and parse request data

        :param req_pattern: use to define attrs of each params,
            eg: {
                    "name": {"type": str, "required": true},
                    "nickname": {"type": str, "default": "zhangsan"},
                    "age": {"type": int, "required": true, "min": 1, "max": 200}
                }
        :return:
        """
        data = dict()
        args = request.args.to_dict()
        if args:
            data.update(args)

        form = request.form.to_dict()
        if form:
            data.update(form)

        body = request.json
        if body:
            data.update(body)

        if req_pattern:
            for k, v in req_pattern.items():
                t = v.get('type')
                if t is None:
                    continue
                # parse request data
                if data.get(k):
                    if type(data[k]) == t:
                        continue
                    if t == int:
                        data[k] = utils.parse_to_int(data[k])
                    elif t == float:
                        data[k] = utils.parse_to_float(data[k])
                    elif t == dict:
                        data[k] = utils.json_loads(data[k])
                    elif t == str:
                        data[k] = utils.parse_to_str(data[k])
                # check required param
                if v.get('required') and data.get(k) is None:
                    return data, error.ParamsError(k)
                # check num min and max
                if t == int or t == float:
                    if v.get('min'):
                        if not isinstance(data.get(k), (int, float)) or data[k] < v['min']:
                            return data, error.ParamsError('%s check min invalid' % k)
                    if v.get('max'):
                        if not isinstance(data.get(k), (int, float)) or data[k] > v['max']:
                            return data, error.ParamsError('%s check max invalid' % k)
                # set default
                if data.get(k) is None and v.get('default') is not None:
                    data[k] = v['default']

        return data, None

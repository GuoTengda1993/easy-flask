#!/usr/bin/env python3
"""parser
Usage, for example:

request:
GET /api?name=xyz&age=10&extra={\"likes\": \"a,b,c,d\"}
parse to data ==>
{
    "name": "xyz",
    "age": 10,
    "extra": {
        "class": "a",
        "likes": ["a", "b", "c", "d"]
    }
}

# -*- code -*-
from flask import request
from easy_flask.utils.parser import parser, Required, Type, Min, Max, Split, Pattern, In, Default

extra_pattern = {
    "class": {Type: str, Default: "a", In: ["a", "b", "c"]},
    "likes": {Type: list, Split: ","}
}
pattern = {
    "name": {Type: str, Required: True},
    "age": {Type: int, Required: True, Min: 1, Max: 200},
    "extra": {Type: dict, Required: True}
}

data, err = parser(data=request.args.to_dict(), pattern=pattern)
...
"""
import json
from json.decoder import JSONDecodeError
from typing import Union


Type = 'type'  # param type: str, int, float, dict, list, bool
Required = 'required'  # if param required, set True
Default = 'default'  # set default value if param is None
Min = 'min'  # check min if param type is int or float
Max = 'max'  # check max if param type is int or float
Split = 'split'  # auto split str to list
In = 'in'  # check value in
Not = 'not'  # check value not
Pattern = 'pattern'  # if Type is dict or list, parse pattern for dict or each item(dict) in list


def parse_to_int(s, minimum: Union[None, int] = None, maximum: Union[None, int] = None):
    """parse unknown data to int, return None when exception

    :param s:
    :param minimum: check min if set
    :param maximum: check max if set
    :return:
    """
    try:
        tmp = int(s)
        if minimum is not None and tmp < minimum:
            return None
        if maximum is not None and tmp > maximum:
            return None
        return tmp
    except (ValueError, TypeError):
        return None


def parse_to_float(s, minimum: Union[None, float] = None, maximum: Union[None, float] = None):
    """parse unknown data to float, return None when exception

    :param s:
    :param minimum: check min if set
    :param maximum: check max if set
    :return:
    """
    try:
        tmp = float(s)
        if minimum is not None and tmp < minimum:
            return None
        if maximum is not None and tmp > maximum:
            return None
        return tmp
    except (ValueError, TypeError):
        return None


def parse_to_str(s):
    """parse object to str

    :param s:
    :return:
    """
    if isinstance(s, (dict, list)):
        return json.dumps(s, ensure_ascii=False)
    else:
        return str(s)


def json_loads(s):
    """load json from string, return None when exception

    :param s:
    :return:
    """
    if isinstance(s, (dict, list)):
        return s
    try:
        return json.loads(s)
    except (JSONDecodeError, TypeError):
        return None


def parser(data: dict, pattern: dict, remove_redundant: bool = False):
    """get and parse request data

    :param data:
    :param pattern: use to define attrs of each params,
        eg: {
                "name": {"type": str, "required": true},
                "nickname": {"type": str, "default": "zhangsan"},
                "age": {"type": int, "required": true, "min": 1, "max": 200}
            }
    :param remove_redundant: remove keys in data but not in pattern
    :return:
    """
    for k, v in pattern.items():
        t = v.get(Type)
        if t is None:
            continue
        # parse request data
        if data.get(k):
            if t == int:
                data[k] = parse_to_int(data[k], minimum=v.get(Min), maximum=v.get(Max))
                if data[k] is None:
                    return None, 'key[%s] parse int error, or check min|max error' % k
            elif t == float:
                data[k] = parse_to_float(data[k], minimum=v.get(Min), maximum=v.get(Max))
                if data[k] is None:
                    return None, 'key[%s] parse float error, or check min|max error' % k
            elif t == dict:
                data[k] = json_loads(data[k])
                if v.get(Pattern):
                    if not data[k]:
                        return None, 'key[%s] parse dict null or empty' % k
                    tmp, err = parser(data=data[k], pattern=v[Pattern])
                    if err:
                        return None, 'key[%s] parse dict error: %s' % (k, err)
            elif t == str:
                tmp = parse_to_str(data[k])
                if v.get(Split):
                    tmp = tmp.split(v[Split])
                data[k] = tmp
            elif t == list:
                if v.get(Split) and isinstance(data[k], str):
                    data[k] = data[k].split(v[Split])
                else:
                    data[k] = json_loads(data[k])
                    if v.get(Pattern):
                        if not isinstance(data[k], list):
                            return None, 'key[%s] parse list error, not list' % k
                        if len(data[k]) > 0:
                            tmp_list = []
                            for item in data[k]:
                                tmp, err = parser(data=item, pattern=v[Pattern])
                                if err:
                                    return None, 'key[%s] parse list error, item parse error: %s' % (k, err)
                                tmp_list.append(tmp)
                            data[k] = tmp_list
            elif t == bool:
                if data[k] in ['true', 'True', 'TRUE', 1, '1']:
                    data[k] = True
                else:
                    data[k] = False
            if data[k] is None:
                return None, 'parse[%s] error' % k

        # check required param
        if v.get(Required) and data.get(k) is None:
            return None, '%s is required' % k

        # check in
        if v.get(In):
            if t == list:
                if set(data[k]).difference(v[In]):
                    return None, 'key[%s] In check error' % k
            else:
                if data[k] not in data[In]:
                    return None, 'key[%s] In check error' % k
        # check not
        if v.get(Not):
            if t == list:
                if set(data[k]) & v[Not]:
                    return None, 'key[%s] Not check error' % k
            else:
                if data[k] in data[In]:
                    return None, 'key[%s] Not check error' % k

        # set default
        if data.get(k) is None and v.get(Default) is not None:
            data[k] = v[Default]

    # remove redundant in data but not in pattern
    if remove_redundant:
        redundant_keys = set(data.keys()).difference(set(pattern.keys()))
        for rk in redundant_keys:
            del data[rk]

    return data, None

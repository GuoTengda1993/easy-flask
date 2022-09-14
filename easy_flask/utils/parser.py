#!/usr/bin/env python3
"""utils

"""
import json
from json.decoder import JSONDecodeError


Type = 'type'  # param type: str, int, float, dict, list, bool
Required = 'required'  # if param required, set True
Default = 'default'  # set default value if param is None
Min = 'min'  # check min if param type is int or float
Max = 'max'  # check max if param type is int or float
Split = 'split'  # auto split str to list
In = 'in'  # check value in
Not = 'not'  # check value not


def parse_to_int(s):
    """parse unknown data to int, return None when exception

    :param s:
    :return:
    """
    try:
        return int(s)
    except ValueError or TypeError:
        return None


def parse_to_float(s):
    """parse unknown data to float, return None when exception

    :param s:
    :return:
    """
    try:
        return float(s)
    except ValueError or TypeError:
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
    except JSONDecodeError or TypeError:
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
            if type(data[k]) == t:
                continue
            if t == int:
                data[k] = parse_to_int(data[k])
            elif t == float:
                data[k] = parse_to_float(data[k])
            elif t == dict:
                data[k] = json_loads(data[k])
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

        # check num min and max
        if t == int or t == float:
            if v.get(Min):
                if not isinstance(data.get(k), (int, float)) or data[k] < v['min']:
                    return None, '%s check min invalid' % k
            if v.get(Max):
                if not isinstance(data.get(k), (int, float)) or data[k] > v['max']:
                    return None, '%s check max invalid' % k
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

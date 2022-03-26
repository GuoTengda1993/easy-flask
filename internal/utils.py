#!/usr/bin/env python3
"""utils

"""
import json
from json.decoder import JSONDecodeError


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
    try:
        return json.loads(s)
    except JSONDecodeError or TypeError:
        return None

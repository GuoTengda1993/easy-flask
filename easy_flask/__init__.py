"""easy_flask

"""
import argparse
import shutil
import re
import os
import sys


__version__ = '0.3.0'


def init_args():
    """init args

    :return:
    """
    description = """easy-flask, use it to make a project quickly. 
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n', '--new', type=str, help='input project name, generate a flask project')

    args = parser.parse_args()
    return args


def check_project_name(name: str):
    """project name example: flask_demo

    :param name:
    :return:
    """
    match = re.match('^[a-zA-z]\w+', name)
    if not match:
        return False
    if name != match.group():
        return False
    return True


def get_path():
    tpl_path = ''
    for p in sys.path:
        if not p.endswith('-packages'):
            continue
        tpl_path = os.path.join(p, 'easy_flask', 'tpl')
        if os.path.exists(tpl_path):
            break
    return tpl_path


def main():
    args = init_args()
    p_name = args.new
    if check_project_name(args.new) is False:
        print('project name invalid(%s), eg: easy_flask' % p_name)
        sys.exit(1)

    curr_dir = os.getcwd()
    src_dir = get_path()
    if not src_dir:
        print('ERROR: cannot find easy-flask in python packages')
        sys.exit(1)
    dest_dir = os.path.join(curr_dir, p_name)

    shutil.copytree(src_dir, dest_dir)
    print('flask project create success, enjoy~')
    sys.exit(0)

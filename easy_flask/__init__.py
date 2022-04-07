"""easy_flask

"""
import argparse
import shutil
import re
import os
import sys


__version__ = '0.2.0'


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
    sp_path = ''
    for p in sys.path:
        if p.endswith('-packages'):
            sp_path = p
            break
    if not sp_path:
        return None

    return os.path.join(sp_path, 'easy_flask')


def main():
    args = init_args()
    p_name = args.new
    if check_project_name(args.new) is False:
        print('project name invalid(%s), eg: easy_flask' % p_name)
        sys.exit(1)

    curr_dir = os.getcwd()
    easy_path = get_path()
    if not easy_path:
        print('ERROR: cannot find easy-flask in python packages')
        sys.exit(1)

    src_dir = os.path.join(easy_path, 'tpl')
    dest_dir = os.path.join(curr_dir, p_name)

    shutil.copytree(src_dir, dest_dir)
    print('flask project create success, enjoy~')
    sys.exit(0)

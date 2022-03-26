"""easy_flask

"""
import argparse
import shutil
import re
import os
import sys


__version__ = '0.1.0'


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
    if 'win' in sys.platform:
        python3_path = os.getenv('PYTHON')
        if not python3_path:
            python3_path = os.getenv('PYTHON3')
        if python3_path:
            if 'python3' in python3_path.lower():
                if 'scripts' in python3_path.lower():
                    easy_path = os.path.join(os.path.dirname(os.path.dirname(python3_path)),
                                             'Lib\\site-packages\\easy_flask\\')
                else:
                    easy_path = os.path.join(python3_path, 'Lib\\site-packages\\easy_flask\\')
        else:
            sys_path = os.getenv('path').split(';')
            for each in sys_path:
                if 'python3' in each.lower() and 'scripts' not in each.lower() and 'site-packages' not in each.lower():
                    python3_path = each
                    break
            easy_path = os.path.join(python3_path, 'Lib\\site-packages\\easy_flask\\')
    elif 'linux' in sys.platform:
        with os.popen('find /usr/local/ -name easy_flask -type d') as lp:
            easy_path = lp.read().strip()
    return easy_path


def main():
    args = init_args()
    p_name = args.new
    if check_project_name(args.new) is False:
        print('project name invalid(%s), eg: easy_flask' % p_name)
        sys.exit(1)

    curr_dir = os.getcwd()
    easy_path = get_path()
    src_dir = os.path.join(easy_path, 'tpl')
    dest_dir = os.path.join(curr_dir, p_name)

    shutil.copytree(src_dir, dest_dir)
    print('flask project create success, enjoy~')
    sys.exit(0)

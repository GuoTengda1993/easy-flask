"""easy_flask

"""
import argparse
import shutil
import re
import os
import sys
from fnmatch import filter
from os.path import isdir, join


__version__ = '1.1.3'


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
    path = ''
    for p in sys.path:
        if not p.endswith('-packages'):
            continue
        path = os.path.join(p, 'easy_flask')
        if os.path.exists(path):
            break
    return path


def include_patterns(*patterns):
    """Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """
    def _ignore_patterns(path, names):
        keep = set(name for pattern in patterns for name in filter(names, pattern))
        ignore = set(name for name in names if name not in keep and not isdir(join(path, name)))
        return ignore
    return _ignore_patterns


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
    shutil.copytree(src_dir, dest_dir, ignore=include_patterns('*.py', '*.ini', '*.sh'))
    
    useless_file = os.path.join(dest_dir, '__init__.py')
    os.remove(useless_file)
    
    print('flask project create success, enjoy~')
    sys.exit(0)

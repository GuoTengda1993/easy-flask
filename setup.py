# -*- coding: utf-8 -*-
import ast
import os
import re

from setuptools import find_packages, setup


# parse version from easy_flask/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_init_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "easy_flask", "__init__.py")
with open(_init_file, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))
filepath = 'README.md'

setup(
    name='easy-flask-restful',
    version=version,
    description="Easy to Make Flask Server",
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    keywords='',
    author='Guo Tengda',
    author_email='ttguotengda@foxmail.com',
    url='https://github.com/GuoTengda1993/easy-flask',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={'easy_flask': ['conf/config.ini', 'control.sh']},
    zip_safe=False,
    install_requires=["Flask>=2.0.0"],
    entry_points={
        'console_scripts': [
            'easy-flask = easy_flask:main',
        ]
    },
    data_files=[filepath]
)

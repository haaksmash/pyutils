#!/usr/bin/env python

import os.path

from distutils.core import setup
from setuptools import find_packages

setup(
    name='utils',
    version='0.8.0',
    description='Python Distribution Utilities',
    long_description=open("README.txt").read() if os.path.isfile("README.txt") else open("README.rst"),
    author='Haak Saxberg',
    author_email='haak.erling@gmail.com',
    url='http://github.com/haaksmash/pyutils',
    packages=find_packages(),
)

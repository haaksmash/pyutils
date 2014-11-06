#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='utils',
    version='0.6',
    description='Python Distribution Utilities',
    long_description=open("README.txt").read(),
    author='Haak Saxberg',
    author_email='haak.erling@gmail.com',
    url='http://github.com/haaksmash/pyutils',
    packages=find_packages(),
)

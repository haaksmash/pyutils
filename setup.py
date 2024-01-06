#!/usr/bin/env python

import os.path

from setuptools import find_packages, setup

setup(
    name='utils',
    version='1.0.2',
    description='A grab-bag of utility functions and objects',
    long_description=open("README.txt").read() if os.path.isfile("README.txt") else open("README.rst").read(),
    author='Haak Saxberg',
    author_email='haak.erling@gmail.com',
    url='http://github.com/haaksmash/pyutils',
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
)

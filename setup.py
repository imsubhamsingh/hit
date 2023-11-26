#!/usr/bin/env python3

from setuptools import setup

setup (name = 'hit',
       version = '1.0.0',
       packages = ['hit'],
       entry_points = {
           'console_scripts' : [
               'hit = hit.cli:main'
           ]
       })

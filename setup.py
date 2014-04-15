#!/usr/bin/env python

from distutils.core import setup

setup(name='DS3 SDK',
    version='2.0',
    description='Python SDK and CLI for DS3',
    author='Ryan Moore, Tim Powell',
    author_email='ryanmo@spectralogic.com',
    packages=['ds3'],
    scripts=['scripts/ds3_cli'])

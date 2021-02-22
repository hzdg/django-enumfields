#!/usr/bin/env python

import os
import re

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_version(fname):
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", read(fname)).group(1)


setup(
    name='django-enumfields',
    version=read_version('enumfields/__init__.py'),
    author='HZDG',
    author_email='webmaster@hzdg.com',
    description='Real Python Enums for Django.',
    license='MIT',
    url='https://github.com/hzdg/django-enumfields',
    long_description=(read('README.rst')),
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ],
)

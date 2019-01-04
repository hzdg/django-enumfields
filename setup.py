#!/usr/bin/env python

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


README = read('README.rst')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '-s']
        self.test_suite = True

    def run_tests(self):
        import pytest
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='django-enumfields',
    version='1.0.0',
    author='HZDG',
    author_email='webmaster@hzdg.com',
    description='Real Python Enums for Django.',
    license='MIT',
    url='https://github.com/hzdg/django-enumfields',
    long_description=README,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    tests_require=[
        'pytest-django',
        'Django',
        'djangorestframework'
    ],
    extras_require={
        ":python_version<'3.4'": ['enum34'],
    },
    cmdclass={'test': PyTest},
)

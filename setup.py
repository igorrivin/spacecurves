#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================
HtmlTestRunner
===============================


.. image:: https://img.shields.io/pypi/v/spacecurves.svg
        :target: https://pypi.python.org/pypi/spacecurves
.. image:: https://img.shields.io/travis/igorrivin/spacecurves.svg
        :target: https://travis-ci.org/igorrivin/spacecurves

Utilities for space curves


Links:
---------
* `Github <https://github.com/igorrivin/spacecurves>`_
"""

from setuptools import setup, find_packages

requirements = ['numpy', 'sortedcontainers']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Igor Rivin",
    author_email='rivin@temple.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Utilities for space curves",
    install_requires=requirements,
    license="MIT license",
    long_description=__doc__,
    include_package_data=True,
    keywords='spacecurves',
    name='spacecurves',
    packages=find_packages(include=['spacecurves']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/igorrivin/spacecurves',
    version='0.1.0',
    zip_safe=False,
)

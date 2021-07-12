from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Utilities for space curves'
LONG_DESCRIPTION = 'Knot and Link Theory utilities (Dowker-Thistlethwaite codes, etc)'

setup(
    name='spacecurves',
    version='0.0.1',
    author='Igor Rivin',
    author_email="<rivin@temple.edu>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'itertools'],

    keywords = ['python', 'topology', 'knots', 'links'],
    classifiers = [
        "Development Status :: Alpha",
        "Intended Audience :: Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Any",
        ],
    )

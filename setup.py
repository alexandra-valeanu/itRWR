# -*- coding: UTF-8 -*-

__author__ = "Cécile Beust, Anthony Baptista, Ozan Ozisik, Anaïs Baudot"
__copyright__ = "Copyright 2023, Cécile Beust, Anthony Baptista, ozan.Ozisik,  Anaïs Baudot"
__email__ = "cecile.beust@etudiant.univ-rennes1.fr, anthony.baptista@qmul.ac.uk, ozan.OZISIK@univ-amu.fr"
__license__ = "MIT"

import codecs
import configparser
from setuptools import setup
from setuptools import find_packages
import os
import sys

config = configparser.RawConfigParser()
config.read(os.path.join('.', 'setup.cfg'))
author = config['metadata']['author']
email = config['metadata']['email']
license = config['metadata']['license']

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

if sys.version_info < (3, 6):
    print("At least Python 3.6 is required.\n", file=sys.stderr)
    exit(1)

try:
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools before installing multixrank.",
          file=sys.stderr)
    exit(1)

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as fin:
    long_description = fin.read()

CLASSIFIERS = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3 :: Only
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Information Analysis
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
"""

# Create list of package data files
def data_files_to_list(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

data_example_file_list = data_files_to_list('itRWR/ToyExample')

setup(
    name='itRWR',
    version=get_version("itRWR/__init__.py"),
    description="",
    author=author,
    author_email=email,
    license=license,
    long_description=long_description,
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    packages=find_packages(),
    package_dir={'itRWR': 'itRWR'},
    package_data={'itRWR': data_example_file_list},
    install_requires=['networkx>=2.8', 'numpy', 'pandas', 'psutil', 'pyyaml', 'scipy', 'multixrank'],
    entry_points={},
)

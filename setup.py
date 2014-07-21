#!/usr/bin/env python
#
# setup for the VCF2Space suite
#
# use the following to install:
# 
# $: python setup.py install
#

import os
from setuptools import setup
from os.path import join, dirname
import src

scripts = ['src/KeggPathway.py', 'src/parse_KGML.py']
long_description = """An (obsolete) parser for KEGG XML files

Install it 

"""


setup(name = 'KEGGParser',
    version = 0.2,
    description = 'KEGG Parser',
    long_description = long_description,
#    long_description = open('README.rst').read(),
    author = "Giovanni M. Dall'Olio + Guillaume Dumas",
    author_email = "giovanni.dallolio@kcl.ac.uk",
    url = 'https://github.com/dalloliogm/kegg-kgml-parser--python-',
    packages=['src'],
#    py_modules = ['KeggPathway'],
#    scripts = scripts,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    keywords='KEGG, pathways, parser',
    license='GPL',

#    data_files = ['README.rst'],
    install_requires=[
#        'setuptools',
        'networkx'
        ],
)




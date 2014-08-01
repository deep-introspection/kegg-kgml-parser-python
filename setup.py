#!/usr/bin/env python
#
# setup for the KEGG Parser
#
# use the following to install:
# 
# $: python setup.py install
#

import os
from setuptools import setup, find_packages

setup(
    name = 'KEGGParser',
    version = 0.3,
    description = 'KEGG Parser',
    long_description = open('README.md').read(),
    author = "Giovanni M. Dall'Olio & Guillaume Dumas",
    author_email = "giovanni.dallolio@kcl.ac.uk",
    url = 'https://github.com/dalloliogm/kegg-kgml-parser--python-',
    package_data = {'': ['*.xml']},
    packages = find_packages(exclude=["tests", "plots","bugs"]),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    keywords='KEGG, pathways, parser',
    license='GPL',

    data_files = ['README.md'],
    install_requires=[
#        'setuptools',
        'networkx'
        ],
)




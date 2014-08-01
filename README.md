# KEGG Parser

A parser for KEGG XML files.

You can install it from the python dist utils:

> sudo python setup.py install

Then in python:

> from keggparser import *

Finally to parse a KGML file:

> parse_KGML.KGML2Graph("data/hsa00510.xml")
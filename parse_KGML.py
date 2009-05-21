#!/usr/bin/env python
"""
Parse a KGML file and put in a PyNetworkX graph

>>> graphfile = 'hsa00510_n-glycan.xml'

>>> graph = KGML2Graph(graphfile)
"""

import xml.etree.ElementTree as ET
import networkx
import logging
logging.basicConfig(level=logging.DEBUG)


def KGML2Graph(xmlfile):
    graph = networkx.Graph()
    nodes = {}
    genes = []
    reactions = {}

    tree = ET.parse(xmlfile)
    for el in tree.getiterator('entry'):
        # get all genes or compounds, and associate ids to names
        if el.attrib['type'] in ('gene', 'compound'):       # something else?

   
    return graph, genes, reactions

if __name__ == '__main__':
    KGML2Graph('hsa00510_n-glycan.xml')

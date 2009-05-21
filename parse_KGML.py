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
        if el.attrib['type'] in ('gene', 'compound', 'map'):       # something else?
            name = el.attrib['name']
            id = el.attrib['id']
#            if nodes.has_key(id):
#                raise TypeError('over writing a key')
            title = el.find('graphics').attrib['name']
            nodes[id] = (name, title, el.attrib['type'])
            if el.attrib['type'] == 'gene':
                graph.add_node(title)

    for rel in tree.getiterator('relation'):
        e1 = rel.attrib['entry1']
        e2 = rel.attrib['entry2']
        print
        print 'e1 ', nodes[e1]
        print 'e2 ', nodes[e2] 
        graph.add_edge(nodes[e1][1], nodes[e2][1])
   
    return graph, nodes, genes, reactions

if __name__ == '__main__':
    KGML2Graph('hsa00510_n-glycan.xml')

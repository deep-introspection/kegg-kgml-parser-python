#!/usr/bin/env python
"""
Parse a KGML file and put in a PyNetworkX graph

>>> graphfile = 'data/hsa00510.xml'

>>> graph = KGML2Graph(graphfile)
"""

import xml.etree.ElementTree as ET
import networkx
import logging
import pylab
#logging.basicConfig(level=logging.DEBUG)

from KeggPathway import KeggPathway#, KeggNode

def KGML2Graph(xmlfile, filter_by = ()):
    """
    Parse a KGML file and return a PyNetworkX graph object

    You can retrieve kgml files from ftp://ftp.genome.jp/pub/kegg/xml/
    (the ko folder is for generic pathways, the organism folder is per species)

    >>> graphfile = 'data/hsa00510.xml'
    >>> graph = KGML2Graph(graphfile)[1]

    the filetype option is used to distinguish between ko files (general and containin ortholog entries) 
    and files which are specific to an organism (e.g. file beginning with hsa etc..)


    KGML2Graph return a KeggPathway object, derived from networkx.LabeledGraph:
    >>> print type(graph)
    <class 'KeggPathway.KeggPathway'>

    You can refer to help(networkx.LabeledGraph) and http://networkx.lanl.gov/reference/classes.labeledgraph.html
    for documentation on methods available.

    To get a list of the nodes, use the .nodes() method
    >>> graph.nodes()[0:5]
    ['ALG8', 'ALG9', 'GCS1', 'ST6GAL1', 'ALG2']
    >>> len(graph.nodes())
    72
    >>> graph.edges()[0:5]
    [('ALG8', 'ALG6'), ('ALG9', 'ALG3'), ('GCS1', 'DAD1'), ('ST6GAL1', 'Other glycan degradation'), ('ALG2', 'ALG1')]

    To get detailed informations on a node, use .get_node:
    >>> graph.get_node('ALG8')
    {'xy': (400, 408), 'type': 'gene'}

    All the annotations (such as node type, etc..), are stored in the .label attribute
    >>> graph.label['ALG8']     #doctest: +ELLIPSIS
    {'xy': (400, 408), 'type': 'gene'}

    To obtain a subgraph with only the genes of the pathway, it is recommended to use get_genes: 
    >>> genes_graph = graph.get_genes()
    >>> genes_graph.edges()[0:4]
    [('ALG8', 'ALG6'), ('ALG9', 'ALG3'), ('GCS1', 'DAD1'), ('ALG2', 'ALG1')]
 
    """
    graph = KeggPathway()
    nodes = {}
    genes = []
    reactions = {}
    relations = {}

    tree = ET.parse(xmlfile)

    organism = tree.find('/').attrib['org']
    if organism == 'ko':
        entriestype = ('ortholog', 'map', 'compound',)
    elif organism == 'ec':
        raise NotImplementedError('Didn\'t implement EC pathways yet')
    else:   # this is an organism-specific pathway
        entriestype = ('gene', 'compound', 'map')
    if filter_by:   # TODO: in principle, this won't be needed anymore. Create a full graph and then use get_genes method.
        entriestype = tuple(filter_by)
#    print entriestype

    # Get pathway title (store it in graph.title)
    graph.title = tree.find('/').attrib['title']
    
    # parse and add nodes
    for el in tree.getiterator('entry'):
        # get all genes or compounds, and associate ids to names
        logging.debug(el.attrib['type'] + ' ' + el.attrib['id'])

        node_type = el.attrib['type']   # can be ('gene', 'compound', 'map'..)
        if node_type in entriestype:       # something else?
            name = el.attrib['name']
            id = el.attrib['id']
#            if nodes.has_key(id):
#                raise TypeError('over writing a key')
            graphics = el.find('graphics')
            node_title = graphics.attrib['name']
            node_x = int(graphics.attrib['x'])  # Storing the original X and Y to recreate KEGG layout
            node_y = int(graphics.attrib['y'])
            logging.debug(node_title)

            # some nodes refer to more than a gene, and have a node_title in the form
            # 'nameofthefirstgene...', e.g. 'ALG2...'
            # As a temporary solution (to investigate more), I am just taking the name
            # of the first gene/entity
            if node_title[-3:] == '...':
                node_title = node_title[:-3]

            nodes[id] = (name, node_title, node_type)
            graph.add_node(node_title, data={'type': node_type, 'xy': (node_x, node_y)})
#    logging.debug(nodes)

    # parse and add relations
    for rel in tree.getiterator('relation'):
        e1 = rel.attrib['entry1']
        e2 = rel.attrib['entry2']
        graph.add_edge(nodes[e1][1], nodes[e2][1])
   
    return tree, graph, nodes, genes, reactions

def plot_starlike(graph):
    pylab.figure()
    networkx.draw_circular(graph)
    pylab.title(graph.title)
    title = graph.title.replace('/', '-') # TODO: which is the proper way to remove / in a filename?
    pylab.savefig('./plots/' + title + '.png')
    pylab.show()


def plot_original(graph):
    pos = {}
    for node in graph.nodes():
        pos[node] = graph.get_node(node)['xy']
    pylab.figure()
    networkx.draw_networkx(graph, pos)
    title = graph.title.replace('/', '-') # TODO: which is the proper way to remove / in a filename?
    pylab.savefig('./plots/' + title + '_original_layout.png')
    pylab.show()


def convert_to_gml(graph):
    """
    write the pathway to the gml format
    - http://www.infosun.fim.uni-passau.de/Graphlet/GML/
    """
    networkx.write_gml(graph, graph.title + '.gml')

if __name__ == '__main__':
    import sys
    import argparse
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='parse a KGML pathway file and convert it to python/gml/image')
    parser.add_argument('-pathwayfile', '--pathway', dest='pathwayfile', type=str, default='data/hsa00510.xml')
    parser.add_argument('-d', '-draw', dest='draw_to_image', action='store_true', default=False)
    parser.add_argument('-c', '-draw_circular', dest='draw_circular', action='store_true', default=False)
    parser.add_argument('-g', '-write_gml', dest='write_gml', action='store_true', default=False)
    args = parser.parse_args()
    logging.debug(args)

    pathwayfile = args.pathwayfile

    (tree, graph, nodes, genes, reactions) = KGML2Graph(pathwayfile)

    if args.draw_circular:
        logging.debug('plotting')
        plot_starlike(graph)    
        plot_starlike(graph.get_genes())    

    if args.draw_to_image:
        plot_original(graph)
        plot_original(graph.get_genes())
    
    if args.write_gml:
        logging.debug('plotting')
        convert_to_gml(graph)

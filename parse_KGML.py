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

    See help(KGMLGraph) for more docs.
    You can refer to help(networkx.LabeledGraph) and http://networkx.lanl.gov/reference/classes.labeledgraph.html
    for documentation on methods available.

    """
    graph = KeggPathway()
    nodes = {}
    genes = []
    graph.reactions = {}
    graph.relations = {}

    tree = ET.parse(xmlfile)

    # Determine whether this is a KO or organism-specific map
    organism = tree.getroot().get('org')
    if organism == 'ko':
        entriestype = ('ortholog', 'map', 'compound',)
    elif organism == 'ec':
        raise NotImplementedError('Didn\'t implement EC pathways yet')
    else:   # this is an organism-specific pathway
        entriestype = ('gene', 'compound', 'map')

    # Get pathway title (store it in graph.title)
    graph.title = tree.getroot().get('title')
    graph.name = tree.getroot().get('name')
    graph.id = tree.getroot().get('id')
    
    # parse and add nodes
    for entry in tree.getiterator('entry'):
        # get all genes or compounds, and associate ids to names
        logging.debug(entry.get('type') + ' ' + entry.get('id'))

        node_type = entry.get('type')   # can be ('gene', 'compound', 'map'..)
        if node_type in entriestype:       # something else?
            name = entry.get('name')
            id = entry.get('id')
#            if nodes.has_key(id):
#                raise TypeError('over writing a key')
            graphics = entry.find('graphics')
            node_title = graphics.get('name')
            node_x = int(graphics.get('x'))  # Storing the original X and Y to recreate KEGG layout
            node_y = int(graphics.get('y'))
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
        e1 = rel.get('entry1')
        e2 = rel.get('entry2')
        graph.add_edge(nodes[e1][1], nodes[e2][1])
        graph.relations[e1+'_'+e2] = rel
   
    for reaction in tree.getiterator('reaction'):
        id = reaction.get('name')
        substrate = reaction.find('substrate').get('name')
        product = reaction.find('product').get('name')
        graph.reactions[reaction] = reaction

    return tree, graph, nodes, genes

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

    (tree, graph, nodes, genes) = KGML2Graph(pathwayfile)

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

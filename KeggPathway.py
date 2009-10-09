#!/usr/bin/env python
"""
Basic class to represent Kegg pathways and nodes.

You can use the function parse_KGML.KGML2Graph to create a KeggPathway object from a KGML file.
"""
import networkx

class KeggPathway(networkx.LabeledDiGraph):
    """
    Represent a Kegg Pathway. Derived from networkx.Digraph

    >>> p = KeggPathway()
    >>> p.add_node('gene1', data={'type': 'gene', })
    >>> p.get_node('gene1')
    {'type': 'gene'}

    We can use parse_KGML.KGML2Graph to obtain a graph object:
    >>> from parse_KGML import KGML2Graph
    >>> graphfile = 'data/hsa00510.xml'
    >>> graph = KGML2Graph(graphfile)[1]


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
    title = ''
    labels = {}
    def add_node(self, n, data=None):   # TODO: in principle, I should redefine all the add_node functions to make sure they contain the right data.
        networkx.LabeledDiGraph.add_node(self, n, data)

    def get_genes(self):
        """
        return a subgraph composed only by the genes

        >>> p = KeggPathway()

        >>> p.add_node('gene1', data={'type': 'gene'})
        >>> p.add_node('compound1', data={'type': 'compound'})

        >>> subgraph = p.get_genes()
        >>> print subgraph.nodes()
        ['gene1']
        """
#        subgraph = self.subgraph([node for node in self.nodes() if self.get_node(node)['type'] == 'gene'])
        genes = []
        labels = {}
        for node in self.nodes():
            if self.get_node(node)['type'] == 'gene':
                genes.append(node)
                labels[node] = self.labels[node]
#            else:
#                self.labels.pop(node)
        subgraph = self.subgraph(genes)
        subgraph.title = self.title + ' (genes)'
        subgraph.labels = labels
        return subgraph

    def __repr__(self):
        return self.title + ' pathway' # TODO: __init__ method to make sure self.title exists

#class KeggNode(str):    # StrMixin? networkx.Node?
#    """
#    A node in a KeggPathway graph.
#
#    Can be a gene, compound, etc..
#    >>> gene1 = KeggNode('gene1')#, nodetype='gene')
#    
#    KeggNodes are derived from str, therefore they can be used as such:
#    >>> gene1.find('g')
#    0
#
#    >>> d = {gene1: 0.2 }
#    >>> d.has_key('gene1')
#    True
#
#    """
#    def __init__(self, name, nodetype=''):
#        self.name = name
#
#        self.nodetype = nodetype  # in ('gene', 'compound', 'ortholog', 'metabolite')
#        self.color = 0
#
#    def __str__(self):
#        """
#        the __repr__ method makes sure that the networkx representation is fine
#        """
#        return self.name
#
#    def __repr__(self):
#        return self.name.__repr__()
#
#    def __eq__(self, other):
#        """
#        >>> gene = KeggNode('gene1')
#        >>> gene == 'gene1'
#        True
#        """
#        return self.name == other
#

#!/usr/bin/env python
"""
Basic class to represent Kegg pathways and nodes.

You can use the function parse_KGML.KGML2Graph to create a KeggPathway object from a KGML file.
"""
import networkx

class KeggPathway(networkx.DiGraph):
    """
    Represent a Kegg Pathway. Derived from networkx.Digraph, it adds:
    - reactions: a dictionary of all the reactions in the file

    >>> p = KeggPathway()
    >>> p.add_node('gene1', data={'type': 'gene', })
    >>> p.['gene1']
    {'type': 'gene'}

    We can use parse_KGML.KGML2Graph to obtain a graph object:
    >>> from parse_KGML import KGML2Graph
    >>> graphfile = 'data/hsa00510.xml'
    >>> graph = KGML2Graph(graphfile)[1]


    To get a list of the nodes, use the .nodes() method
    >>> graph.nodes()[0:5]
    ['56', '54', '42', '48', '43']
    >>> len(graph.nodes())
    76
    >>> print [graph.node[n]['label'] for n in graph.nodes()][0:5]
    ['MGAT1', 'MGAT2', 'C01246', 'TITLE:N-Glycan biosynthesis', 'C03862']

    >>> graph.edges()[0:5]
    [('56', '57'), ('54', '55'), ('54', '37'), ('54', '58'), ('60', '62')]

    To get detailed informations on a node, use .node:
    >>> graph.node['10']
    {'xy': (580, 317), 'type': 'gene', 'label': 'ALG12'}

    All the annotations (such as node type, etc..), are stored in the .label attribute
    >>> graph.label['10']     #doctest: +ELLIPSIS
    {'xy': (580, 317), 'type': 'gene', 'label': 'ALG12'}

    To obtain a subgraph with only the genes of the pathway, it is recommended to use get_genes: 
    >>> genes_graph = graph.get_genes()
    >>> genes_graph.edges()[0:4]
    [('60', '62'), ('63', '3'), ('63', '2'), ('63', '72')]

    >>> for (node1, node2) in genes_graph.edges()[0:4]:
    ...     print genes_graph.node[node1]['label'], genes_graph.node[node2]['label']
    GCS1 DAD1...
    ALG5 DPM2
    ALG5 DPM3
    ALG5 DPAGT1

 
 
    """
    title = ''
    labels = {}
    reactions = {}
    def add_node(self, n, data=None):   # TODO: in principle, I should redefine all the add_node functions to make sure they contain the right data.
        networkx.DiGraph.add_node(self, n, data)

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
#        subgraph = self.subgraph([node for node in self.nodes() if self.node[node]['type'] == 'gene'])
        genes = []
        labels = {}
        for n in self.nodes():
            if self.node[n]['type'] == 'gene':
                genes.append(n)
                labels[n] = self.node[n]
#            else:
#                self.labels.pop(node)
        subgraph = self.subgraph(genes)
        subgraph.title = self.title + ' (genes)'
        subgraph.labels = labels
        return subgraph

    def neighbors_labels(self, node):
        """
        like networkx.graph.neighbours, but returns gene label

        >>> p = KeggPathway()

        >>> p.add_node(1, data={'label': 'gene1'})
        >>> p.add_node(2, data={'label': 'gene2'})
        >>> p.add_edge(1, 2)

        >>> p.neighbors(1)
        [2]

        >>> p.neighbors_labels(1)
        {'gene1': ['gene2']}
        """
        neighbours = self.neighbors(node)
        labels = [self.node[n]['label'] for n in neighbours]
        return {self.node[node]['label']: labels}


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

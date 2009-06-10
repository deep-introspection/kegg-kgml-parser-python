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

#    >>> p.get_node('gene1')

    """
    def add_node(self, n, data=None):   # TODO: in principle, I should redefine all the add_node functions to make sure they contain the right data.
        networkx.LabeledDiGraph.add_node(self, n, data)

    def get_genes(self):
        """
        return a subgraph composed only of the genes

        >>> p = KeggPathway()

        >>> p.add_node('gene1', data={'type': 'gene'})
        >>> p.add_node('compound1', data={'type': 'compound'})

        >>> subgraph = p.get_genes()
        >>> print subgraph.nodes()
        ['gene1']
        """
        return self.subgraph([node for node in self.nodes() if self.get_node(node)['type'] == 'gene'])

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

#!/usr/bin/env python
"""
Basic class to represent Kegg pathways and nodes.

You can use the function parse_KGML.KGML2Graph to create a KeggPathway object from a KGML file.
"""
import networkx

class KeggPathway(networkx.DiGraph):
    """
    Represent a Kegg Pathway. Derived from networkx.Digraph

    >>> pw = KeggPathway()
    >>> pw.add_node('gene1')    # add_node will be modified to automatically 
    ...                         # convert all nodes in KeggNode objects

    """
    def add_node(self, n):
        """
        redefining add_node.
        """
        n = KeggNode(n)

        # TODO: call the original function instead of rewriting it
        if n not in self.succ:
            self.succ[n] = {}
            self.pred[n] = {}


class KeggNode(str):    # StrMixin? networkx.Node?
    """
    A node in a KeggPathway graph.

    Can be a gene, compound, etc..
    >>> 
    """
    def __init__(self, name, nodetype=''):
        self.name = name

        self.type = nodetype  # in ('gene', 'compound', 
        self.color = 0

    def __str__(self):
        """
        the __repr__ method makes sure that the networkx representation is fine
        """
        return self.name

    def __repr__(self):
        return self.name.__repr__()

    def __eq__(self, other):
        """
        >>> gene = KeggNode('gene1')
        >>> gene == 'gene1'
        True
        """
        return self.name == other


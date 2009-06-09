#!/usr/bin/env python
"""
Basic class to represent Kegg pathways and nodes.

You can use the function parse_KGML.KGML2Graph to create a KeggPathway object from a KGML file.
"""

class KeggPathway(networkx.DiGraph):
    """
    Represent a Kegg Pathway. Derived from networkx.Digraph

    >>> pw = KeggPathway()
    >>> pw.add_node('gene1')    # add_node will be modified to automatically 
                                # convert all nodes in KeggNode objects

    """
    pass

class KeggNode(object):
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




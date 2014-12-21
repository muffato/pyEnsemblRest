
def _tax_parent(self):
    if '_parent' not in self.__dict__:
        if not hasattr(self, '_id'):
            print("'id' is not defined, cannot fetch the parent node")
            return None
        copy = self.server.getTaxonomyEntryByID(self.id)
        self.__dict__['_parent'] = copy.__dict__['_parent']
    return self.__dict__['_parent']


import ensembl

class GeneTree(ensembl.BaseObject):
    """Global object for gene-trees"""

    #id = property(lambda self : getattr(self, "_id"), None, None, """GeneTree stable identifier""")
    id = property(lambda self : getattr(self, "_id"), lambda self, val : setattr(self, "_id", val), None, """GeneTree stable identifier""")

class GeneTreeNode(ensembl.BaseObject):
    """Node in a gene-tree"""

class GeneTreeNodeConfidence(ensembl.BaseObject):
    """The confidence tags attached to a given gene-tree node"""

class GeneTreeMember(ensembl.BaseObject):
    """Used in gene-tree leaves to show the actual protein that was used to build the tree"""

class GeneTreeEvent(ensembl.BaseObject):
    """The evolutionary event that took place at this node of the tree"""

class NCBITaxon(ensembl.BaseObject):
    """A node in the NCBI taxonomy"""

    #parent = property(_tax_parent, None, None, """Parent node in the taxonomy""")
    parent = property(_tax_parent, lambda self, val : setattr(self, "_parent", val), None, """Parent node in the taxonomy""")

class MethodLinkSpeciesSet(ensembl.BaseObject):
    """"""

class HomologyGroup(ensembl.BaseObject):
    """Group of multiple homology-pairs"""

class HomologyPair(ensembl.BaseObject):
    """Homology pair"""

class Homolog(ensembl.BaseObject):
    """"""

class GenomicAlignment(ensembl.BaseObject):
    """"""

class GenomicAlignmentEntry(ensembl.BaseObject):
    """"""


def _gtn_get_all_leaves(self):
    """
        Get all the leaves under this node
    """
    if '_children' not in self.__dict__:
        return [self]
    l = []
    for n in self.children:
        l.extend(n.get_all_leaves())
    return l

setattr(GeneTreeNode, 'get_all_leaves', _gtn_get_all_leaves)



def _gt_get_all_leaves(self):
    """
        Get all the leaves in this tree
    """
    return self.tree.get_all_leaves()

setattr(GeneTree, 'get_all_leaves', _gt_get_all_leaves)




def _tax_parent(self):
    if '_parent' not in self.__dict__:
        if not hasattr(self, '_id'):
            print("'id' is not defined, cannot fetch the parent node")
            return None
        copy = self.server.getTaxonomyEntryByID(self.id)
        self.__dict__['_parent'] = copy.__dict__['_parent']
    return self.__dict__['_parent']

def _tax_children(self):
    if self.leaf:
        return []
    if '_children' not in self.__dict__:
        if not hasattr(self, '_id'):
            print("'id' is not defined, cannot fetch the parent node")
            return []
        copy = self.server.getTaxonomyEntryByID(self.id)
        self.__dict__['_children'] = copy.__dict__['_children']
    return self.__dict__['_children']



from . import genome
from . import _pyrest_core

class NCBITaxon(_pyrest_core.BaseObject):
    """A node in the NCBI taxonomy"""

    parent = property(_tax_parent, None, None, """Parent node in the taxonomy""")

    children = property(_tax_children, None, None, """Child nodes in the taxonomy""")

    tags = property(_pyrest_core.fget("_tags"), None, None, """Additionnal tags""")

NCBITaxon._construction_rules = {"children":NCBITaxon, "parent":NCBITaxon, "tags":None}

class GeneTreeMember(_pyrest_core.BaseObject):
    """A leaf of a gene-tree, i.e. a protein / gene"""

    id = property(_pyrest_core.fget("_id"), None, None, """Protein / transcript identifier""")

    mol_seq = property(_pyrest_core.fget("_mol_seq"), None, None, """DNA / protein sequence""")

GeneTreeMember._construction_rules = {"id":genome.Identifier, "mol_seq":genome.Sequence}

class GeneTreeEvent(_pyrest_core.BaseObject):
    """The evolutionary event that took place at this node of the tree"""

class GeneTreeNode(_pyrest_core.BaseObject):
    """Node in a gene-tree"""

    taxonomy = property(_pyrest_core.fget("_taxonomy"), None, None, """Taxonomy annotation of this node""")

    children = property(_pyrest_core.fget("_children"), None, None, """Child nodes in the gene-tree""")

    confidence = property(_pyrest_core.fget("_confidence"), None, None, """The confidence tags attached to a given gene-tree node""")

    id = property(_pyrest_core.fget("_id"), None, None, """Gene identifier (only for leaves)""")

    events = property(_pyrest_core.fget("_events"), None, None, """The evolutionary event that took place at this node""")

    sequence = property(_pyrest_core.fget("_sequence"), None, None, """GeneTreeMember (only for leaves)""")

GeneTreeNode._construction_rules = {"children":GeneTreeNode, "confidence":None, "events":GeneTreeEvent, "id":genome.Identifier, "sequence":GeneTreeMember, "taxonomy":NCBITaxon}

class GeneTree(_pyrest_core.BaseObject):
    """Global object for gene-trees"""

    tree = property(_pyrest_core.fget("_tree"), None, None, """root node""")

    id = property(_pyrest_core.fget("_id"), None, None, """GeneTree stable identifier""")

GeneTree._construction_rules = {"tree":GeneTreeNode}

class MethodLinkSpeciesSet(_pyrest_core.BaseObject):
    """"""

class Homolog(_pyrest_core.BaseObject):
    """"""

class HomologyPair(_pyrest_core.BaseObject):
    """Homology pair"""

    target = property(_pyrest_core.fget("_target"), None, None, """Paralog of the query gene / Ortholog in the other species""")

    source = property(_pyrest_core.fget("_source"), None, None, """Query gene""")

HomologyPair._construction_rules = {"source":Homolog, "target":Homolog}

class HomologyGroup(_pyrest_core.BaseObject):
    """Group of multiple homology-pairs"""

    homologies = property(_pyrest_core.fget("_homologies"), None, None, """All the homology pairs""")

HomologyGroup._construction_rules = {"homologies":HomologyPair}

class GenomicAlignmentEntry(_pyrest_core.BaseObject):
    """"""

class GenomicAlignment(_pyrest_core.BaseObject):
    """"""

    alignments = property(_pyrest_core.fget("_alignments"), None, None, """All the alignment-bloks for this query region""")

GenomicAlignment._construction_rules = {"alignments":GenomicAlignmentEntry}


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

def _gtn_get_all_nodes(self):
    """
        Get all the nodes in this sub-tree, including the root
    """
    if '_children' not in self.__dict__:
        return [self]
    l = [self]
    for n in self.children:
        l.extend(n.get_all_nodes())
    return l

setattr(GeneTreeNode, 'get_all_nodes', _gtn_get_all_nodes)

def _gt_get_all_leaves(self):
    """
        Get all the leaves in this tree
    """
    return self.tree.get_all_leaves()

setattr(GeneTree, 'get_all_leaves', _gt_get_all_leaves)

def _gt_get_all_nodes(self):
    """
        Get all the nodes in this tree
    """
    return self.tree.get_all_nodes()

setattr(GeneTree, 'get_all_nodes', _gt_get_all_nodes)



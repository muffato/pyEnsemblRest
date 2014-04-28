import ensembl

class GeneTree(ensembl.BaseObject):
	"""Global object for gene-trees"""

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

def _gtn_get_all_leaves(self):
	"""
		Get all the leaves under this node
	"""
	if 'children' not in self.__dict__:
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



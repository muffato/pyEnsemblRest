
import ensembl

class GeneTree(ensembl.BaseObject):
	"""
		Class for gene-trees
	"""

	def get_all_leaves(self):
		"""
			Get all the leaves
		"""
		return self.tree.get_all_leaves()

class GeneTreeNode(ensembl.BaseObject):
	"""
		Class for gene-tree nodes
	"""

	def get_all_leaves(self):
		if 'children' not in self.__dict__:
			return [self]
		l = []
		for n in self.children:
			l.extend(n.get_all_leaves())
		return l

class NCBITaxon(ensembl.BaseObject):
	pass

class GeneTreeEvent(ensembl.BaseObject):
	pass

class GeneTreeNodeConfidence(ensembl.BaseObject):
	pass

class GeneTreeMember(ensembl.BaseObject):
	pass

import ensembl.genome

ensembl._pyrest.construction_rules.update({
	(GeneTree, 'tree') : GeneTreeNode,
	(GeneTreeNode, 'taxonomy') : NCBITaxon,
	(GeneTreeNode, 'events') : GeneTreeEvent,
	(GeneTreeNode, 'confidence') : GeneTreeNodeConfidence,
	(GeneTreeNode, 'children') : GeneTreeNode,
	(GeneTreeNode, 'sequence') : GeneTreeMember,
	(GeneTreeNode, 'id') : ensembl.genome.Identifier,
	(GeneTreeMember, 'id') : ensembl.genome.Identifier,
	(GeneTreeMember, 'mol_seq') : ensembl.genome.Sequence
})


ensembl._pyrest.endpoint_2_class.update({
	'/genetree/id/' : GeneTree,
	'/genetree/member/id/' : GeneTree,
	'/genetree/member/symbol/' : GeneTree
})



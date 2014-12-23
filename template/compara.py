
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



#__GENERATED_OBJECTS__

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


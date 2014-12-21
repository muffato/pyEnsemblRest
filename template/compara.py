
def _tax_parent(self):
    if '_parent' not in self.__dict__:
        if not hasattr(self, '_id'):
            print("'id' is not defined, cannot fetch the parent node")
            return None
        copy = self.server.getTaxonomyEntryByID(self.id)
        self.__dict__['_parent'] = copy.__dict__['_parent']
    return self.__dict__['_parent']


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



def _gt_get_all_leaves(self):
    """
        Get all the leaves in this tree
    """
    return self.tree.get_all_leaves()

setattr(GeneTree, 'get_all_leaves', _gt_get_all_leaves)


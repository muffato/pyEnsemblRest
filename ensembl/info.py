import ensembl

class SeqRegion(ensembl.BaseObject):
    """"""

class Assembly(ensembl.BaseObject):
    """"""

    #top_level_region = property(lambda self : getattr(self, "_top_level_region"), None, None, """None""")
    top_level_region = property(lambda self : getattr(self, "_top_level_region"), lambda self, val : setattr(self, "_top_level_region", val), None, """None""")

Assembly._construction_rules = {"top_level_region":SeqRegion}

class ArchiveEntry(ensembl.BaseObject):
    """"""

class Species(ensembl.BaseObject):
    """"""

class ExternalDatabase(ensembl.BaseObject):
    """"""

class Biotype(ensembl.BaseObject):
    """"""

class OntologyTerm(ensembl.BaseObject):
    """"""

    #children = property(lambda self : getattr(self, "_children"), None, None, """None""")
    children = property(lambda self : getattr(self, "_children"), lambda self, val : setattr(self, "_children", val), None, """None""")

    #parents = property(lambda self : getattr(self, "_parents"), None, None, """None""")
    parents = property(lambda self : getattr(self, "_parents"), lambda self, val : setattr(self, "_parents", val), None, """None""")

OntologyTerm._construction_rules = {"children":OntologyTerm, "parents":OntologyTerm}

class OntologyEntry(ensembl.BaseObject):
    """"""

    #is_a = property(lambda self : getattr(self, "_is_a"), None, None, """None""")
    is_a = property(lambda self : getattr(self, "_is_a"), lambda self, val : setattr(self, "_is_a", val), None, """None""")

    #term = property(lambda self : getattr(self, "_term"), None, None, """None""")
    term = property(lambda self : getattr(self, "_term"), lambda self, val : setattr(self, "_term", val), None, """None""")

OntologyEntry._construction_rules = {"is_a":OntologyTerm, "term":OntologyTerm}


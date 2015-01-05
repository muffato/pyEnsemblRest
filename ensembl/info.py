from . import _pyrest_core

class SeqRegion(_pyrest_core.BaseObject):
    """"""

class Assembly(_pyrest_core.BaseObject):
    """"""

    #top_level_region = property(lambda self : getattr(self, "_top_level_region"), None, None, """No documentation""")
    top_level_region = property(lambda self : getattr(self, "_top_level_region"), lambda self, val : setattr(self, "_top_level_region", val), None, """No documentation""")

Assembly._construction_rules = {"top_level_region":SeqRegion}

class ArchiveEntry(_pyrest_core.BaseObject):
    """"""

class Species(_pyrest_core.BaseObject):
    """"""

class ExternalDatabase(_pyrest_core.BaseObject):
    """"""

class Biotype(_pyrest_core.BaseObject):
    """"""

class OntologyTerm(_pyrest_core.BaseObject):
    """"""

    #children = property(lambda self : getattr(self, "_children"), None, None, """No documentation""")
    children = property(lambda self : getattr(self, "_children"), lambda self, val : setattr(self, "_children", val), None, """No documentation""")

    #parents = property(lambda self : getattr(self, "_parents"), None, None, """No documentation""")
    parents = property(lambda self : getattr(self, "_parents"), lambda self, val : setattr(self, "_parents", val), None, """No documentation""")

OntologyTerm._construction_rules = {"children":OntologyTerm, "parents":OntologyTerm}

class OntologyEntry(_pyrest_core.BaseObject):
    """"""

    #is_a = property(lambda self : getattr(self, "_is_a"), None, None, """No documentation""")
    is_a = property(lambda self : getattr(self, "_is_a"), lambda self, val : setattr(self, "_is_a", val), None, """No documentation""")

    #term = property(lambda self : getattr(self, "_term"), None, None, """No documentation""")
    term = property(lambda self : getattr(self, "_term"), lambda self, val : setattr(self, "_term", val), None, """No documentation""")

OntologyEntry._construction_rules = {"is_a":OntologyTerm, "term":OntologyTerm}


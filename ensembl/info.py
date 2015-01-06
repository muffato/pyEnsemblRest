from . import _pyrest_core

class SeqRegion(_pyrest_core.BaseObject):
    """"""

class Assembly(_pyrest_core.BaseObject):
    """"""

    top_level_region = property(_pyrest_core.fget("_top_level_region"), None, None, """No documentation""")

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

    children = property(_pyrest_core.fget("_children"), None, None, """No documentation""")

    parents = property(_pyrest_core.fget("_parents"), None, None, """No documentation""")

OntologyTerm._construction_rules = {"children":OntologyTerm, "parents":OntologyTerm}

class OntologyEntry(_pyrest_core.BaseObject):
    """"""

    is_a = property(_pyrest_core.fget("_is_a"), None, None, """No documentation""")

    term = property(_pyrest_core.fget("_term"), None, None, """No documentation""")

OntologyEntry._construction_rules = {"is_a":OntologyTerm, "term":OntologyTerm}


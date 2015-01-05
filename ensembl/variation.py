from . import genome
from . import _pyrest_core

class AlleleLocation(genome.Location):
    """"""

class Genotype(_pyrest_core.BaseObject):
    """"""

class PopulationGenotype(_pyrest_core.BaseObject):
    """"""

class PopulationAllele(_pyrest_core.BaseObject):
    """"""

class Variation(_pyrest_core.BaseObject):
    """"""

    #population_genotypes = property(lambda self : getattr(self, "_population_genotypes"), None, None, """No documentation""")
    population_genotypes = property(lambda self : getattr(self, "_population_genotypes"), lambda self, val : setattr(self, "_population_genotypes", val), None, """No documentation""")

    #populations = property(lambda self : getattr(self, "_populations"), None, None, """No documentation""")
    populations = property(lambda self : getattr(self, "_populations"), lambda self, val : setattr(self, "_populations", val), None, """No documentation""")

    #genotypes = property(lambda self : getattr(self, "_genotypes"), None, None, """No documentation""")
    genotypes = property(lambda self : getattr(self, "_genotypes"), lambda self, val : setattr(self, "_genotypes", val), None, """No documentation""")

    #mappings = property(lambda self : getattr(self, "_mappings"), None, None, """No documentation""")
    mappings = property(lambda self : getattr(self, "_mappings"), lambda self, val : setattr(self, "_mappings", val), None, """No documentation""")

Variation._construction_rules = {"genotypes":Genotype, "mappings":AlleleLocation, "population_genotypes":PopulationGenotype, "populations":PopulationAllele}

class Consequence(_pyrest_core.BaseObject):
    """"""

class Variant(_pyrest_core.BaseObject):
    """"""

class VEPResult(_pyrest_core.BaseObject):
    """"""

    #colocated_variants = property(lambda self : getattr(self, "_colocated_variants"), None, None, """No documentation""")
    colocated_variants = property(lambda self : getattr(self, "_colocated_variants"), lambda self, val : setattr(self, "_colocated_variants", val), None, """No documentation""")

    #transcript_consequences = property(lambda self : getattr(self, "_transcript_consequences"), None, None, """No documentation""")
    transcript_consequences = property(lambda self : getattr(self, "_transcript_consequences"), lambda self, val : setattr(self, "_transcript_consequences", val), None, """No documentation""")

VEPResult._construction_rules = {"colocated_variants":Variant, "transcript_consequences":Consequence}


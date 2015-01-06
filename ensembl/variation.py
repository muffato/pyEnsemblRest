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

    population_genotypes = property(_pyrest_core.fget("_population_genotypes"), None, None, """No documentation""")

    populations = property(_pyrest_core.fget("_populations"), None, None, """No documentation""")

    genotypes = property(_pyrest_core.fget("_genotypes"), None, None, """No documentation""")

    mappings = property(_pyrest_core.fget("_mappings"), None, None, """No documentation""")

Variation._construction_rules = {"genotypes":Genotype, "mappings":AlleleLocation, "population_genotypes":PopulationGenotype, "populations":PopulationAllele}

class Consequence(_pyrest_core.BaseObject):
    """"""

class Variant(_pyrest_core.BaseObject):
    """"""

class VEPResult(_pyrest_core.BaseObject):
    """"""

    colocated_variants = property(_pyrest_core.fget("_colocated_variants"), None, None, """No documentation""")

    transcript_consequences = property(_pyrest_core.fget("_transcript_consequences"), None, None, """No documentation""")

VEPResult._construction_rules = {"colocated_variants":Variant, "transcript_consequences":Consequence}


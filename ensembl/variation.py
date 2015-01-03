import ensembl

class AlleleLocation(ensembl.genome.Location):
    """"""

class Genotype(ensembl.BaseObject):
    """"""

class PopulationGenotype(ensembl.BaseObject):
    """"""

class PopulationAllele(ensembl.BaseObject):
    """"""

class Variation(ensembl.BaseObject):
    """"""

    #population_genotypes = property(lambda self : getattr(self, "_population_genotypes"), None, None, """None""")
    population_genotypes = property(lambda self : getattr(self, "_population_genotypes"), lambda self, val : setattr(self, "_population_genotypes", val), None, """None""")

    #populations = property(lambda self : getattr(self, "_populations"), None, None, """None""")
    populations = property(lambda self : getattr(self, "_populations"), lambda self, val : setattr(self, "_populations", val), None, """None""")

    #genotypes = property(lambda self : getattr(self, "_genotypes"), None, None, """None""")
    genotypes = property(lambda self : getattr(self, "_genotypes"), lambda self, val : setattr(self, "_genotypes", val), None, """None""")

    #mappings = property(lambda self : getattr(self, "_mappings"), None, None, """None""")
    mappings = property(lambda self : getattr(self, "_mappings"), lambda self, val : setattr(self, "_mappings", val), None, """None""")

Variation._construction_rules = {"population_genotypes":PopulationGenotype, "genotypes":Genotype, "mappings":AlleleLocation, "populations":PopulationAllele}

class Consequence(ensembl.BaseObject):
    """"""

class Variant(ensembl.BaseObject):
    """"""

class VEPResult(ensembl.BaseObject):
    """"""

    #colocated_variants = property(lambda self : getattr(self, "_colocated_variants"), None, None, """None""")
    colocated_variants = property(lambda self : getattr(self, "_colocated_variants"), lambda self, val : setattr(self, "_colocated_variants", val), None, """None""")

    #transcript_consequences = property(lambda self : getattr(self, "_transcript_consequences"), None, None, """None""")
    transcript_consequences = property(lambda self : getattr(self, "_transcript_consequences"), lambda self, val : setattr(self, "_transcript_consequences", val), None, """None""")

VEPResult._construction_rules = {"transcript_consequences":Consequence, "colocated_variants":Variant}


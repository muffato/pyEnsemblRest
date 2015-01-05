
from . import _pyrest_core

class Identifier(_pyrest_core.BaseObject):
    """"""

class Sequence(_pyrest_core.BaseObject):
    """"""

class Feature(_pyrest_core.BaseObject):
    """"""

    #seq_region_name = property(lambda self : getattr(self, "_seq_region_name"), None, None, """Name of the chromosome, scaffold, etc the feature is on""")
    seq_region_name = property(lambda self : getattr(self, "_seq_region_name"), lambda self, val : setattr(self, "_seq_region_name", val), None, """Name of the chromosome, scaffold, etc the feature is on""")

    #feature_type = property(lambda self : getattr(self, "_feature_type"), None, None, """Type of this feature, usually redundant with the class itself (e.g. ExonFeature, TranscriptFeature, etc)""")
    feature_type = property(lambda self : getattr(self, "_feature_type"), lambda self, val : setattr(self, "_feature_type", val), None, """Type of this feature, usually redundant with the class itself (e.g. ExonFeature, TranscriptFeature, etc)""")

    #start = property(lambda self : getattr(self, "_start"), None, None, """Start coordinate""")
    start = property(lambda self : getattr(self, "_start"), lambda self, val : setattr(self, "_start", val), None, """Start coordinate""")

    #end = property(lambda self : getattr(self, "_end"), None, None, """End coordinate""")
    end = property(lambda self : getattr(self, "_end"), lambda self, val : setattr(self, "_end", val), None, """End coordinate""")

    #strand = property(lambda self : getattr(self, "_strand"), None, None, """Strand""")
    strand = property(lambda self : getattr(self, "_strand"), lambda self, val : setattr(self, "_strand", val), None, """Strand""")

    #assembly_name = property(lambda self : getattr(self, "_assembly_name"), None, None, """Name of the genome assembly""")
    assembly_name = property(lambda self : getattr(self, "_assembly_name"), lambda self, val : setattr(self, "_assembly_name", val), None, """Name of the genome assembly""")

class FeatureWithID(Feature):
    """"""

    #id = property(lambda self : getattr(self, "_id"), None, None, """No documentation""")
    id = property(lambda self : getattr(self, "_id"), lambda self, val : setattr(self, "_id", val), None, """No documentation""")

class ExonFeature(FeatureWithID):
    """"""

    #source = property(lambda self : getattr(self, "_source"), None, None, """No documentation""")
    source = property(lambda self : getattr(self, "_source"), lambda self, val : setattr(self, "_source", val), None, """No documentation""")

    #constitutive = property(lambda self : getattr(self, "_constitutive"), None, None, """No documentation""")
    constitutive = property(lambda self : getattr(self, "_constitutive"), lambda self, val : setattr(self, "_constitutive", val), None, """No documentation""")

    #ensembl_phase = property(lambda self : getattr(self, "_ensembl_phase"), None, None, """No documentation""")
    ensembl_phase = property(lambda self : getattr(self, "_ensembl_phase"), lambda self, val : setattr(self, "_ensembl_phase", val), None, """No documentation""")

    #ensembl_end_phase = property(lambda self : getattr(self, "_ensembl_end_phase"), None, None, """No documentation""")
    ensembl_end_phase = property(lambda self : getattr(self, "_ensembl_end_phase"), lambda self, val : setattr(self, "_ensembl_end_phase", val), None, """No documentation""")

    #parent = property(lambda self : getattr(self, "_parent"), None, None, """No documentation""")
    parent = property(lambda self : getattr(self, "_parent"), lambda self, val : setattr(self, "_parent", val), None, """No documentation""")

    #version = property(lambda self : getattr(self, "_version"), None, None, """No documentation""")
    version = property(lambda self : getattr(self, "_version"), lambda self, val : setattr(self, "_version", val), None, """No documentation""")

    #rank = property(lambda self : getattr(self, "_rank"), None, None, """No documentation""")
    rank = property(lambda self : getattr(self, "_rank"), lambda self, val : setattr(self, "_rank", val), None, """No documentation""")

class TranslationFeature(FeatureWithID):
    """"""

    #description = property(lambda self : getattr(self, "_description"), None, None, """No documentation""")
    description = property(lambda self : getattr(self, "_description"), lambda self, val : setattr(self, "_description", val), None, """No documentation""")

    #parent = property(lambda self : getattr(self, "_parent"), None, None, """No documentation""")
    parent = property(lambda self : getattr(self, "_parent"), lambda self, val : setattr(self, "_parent", val), None, """No documentation""")

    #interpro = property(lambda self : getattr(self, "_interpro"), None, None, """No documentation""")
    interpro = property(lambda self : getattr(self, "_interpro"), lambda self, val : setattr(self, "_interpro", val), None, """No documentation""")

    #type = property(lambda self : getattr(self, "_type"), None, None, """No documentation""")
    type = property(lambda self : getattr(self, "_type"), lambda self, val : setattr(self, "_type", val), None, """No documentation""")

class FeatureLikeBiotype(FeatureWithID):
    """"""

    #biotype = property(lambda self : getattr(self, "_biotype"), None, None, """No documentation""")
    biotype = property(lambda self : getattr(self, "_biotype"), lambda self, val : setattr(self, "_biotype", val), None, """No documentation""")

    #external_name = property(lambda self : getattr(self, "_external_name"), None, None, """No documentation""")
    external_name = property(lambda self : getattr(self, "_external_name"), lambda self, val : setattr(self, "_external_name", val), None, """No documentation""")

    #description = property(lambda self : getattr(self, "_description"), None, None, """No documentation""")
    description = property(lambda self : getattr(self, "_description"), lambda self, val : setattr(self, "_description", val), None, """No documentation""")

    #source = property(lambda self : getattr(self, "_source"), None, None, """No documentation""")
    source = property(lambda self : getattr(self, "_source"), lambda self, val : setattr(self, "_source", val), None, """No documentation""")

    #version = property(lambda self : getattr(self, "_version"), None, None, """No documentation""")
    version = property(lambda self : getattr(self, "_version"), lambda self, val : setattr(self, "_version", val), None, """No documentation""")

    #logic_name = property(lambda self : getattr(self, "_logic_name"), None, None, """No documentation""")
    logic_name = property(lambda self : getattr(self, "_logic_name"), lambda self, val : setattr(self, "_logic_name", val), None, """No documentation""")

class TranscriptFeature(FeatureLikeBiotype):
    """"""

    #translation = property(lambda self : getattr(self, "_translation"), None, None, """No documentation""")
    translation = property(lambda self : getattr(self, "_translation"), lambda self, val : setattr(self, "_translation", val), None, """No documentation""")

    #exon = property(lambda self : getattr(self, "_exon"), None, None, """No documentation""")
    exon = property(lambda self : getattr(self, "_exon"), lambda self, val : setattr(self, "_exon", val), None, """No documentation""")

    #parent = property(lambda self : getattr(self, "_parent"), None, None, """No documentation""")
    parent = property(lambda self : getattr(self, "_parent"), lambda self, val : setattr(self, "_parent", val), None, """No documentation""")

TranscriptFeature._construction_rules = {"exon":ExonFeature, "translation":TranslationFeature}

class GeneFeature(FeatureLikeBiotype):
    """"""

    #transcript = property(lambda self : getattr(self, "_transcript"), None, None, """No documentation""")
    transcript = property(lambda self : getattr(self, "_transcript"), lambda self, val : setattr(self, "_transcript", val), None, """No documentation""")

GeneFeature._construction_rules = {"transcript":TranscriptFeature}

class ChipSeqFeature(Feature):
    """"""

    #chipseq_feature_type = property(lambda self : getattr(self, "_chipseq_feature_type"), None, None, """ChipSeq type""")
    chipseq_feature_type = property(lambda self : getattr(self, "_chipseq_feature_type"), lambda self, val : setattr(self, "_chipseq_feature_type", val), None, """ChipSeq type""")

    #cell_type = property(lambda self : getattr(self, "_cell_type"), None, None, """Cell type""")
    cell_type = property(lambda self : getattr(self, "_cell_type"), lambda self, val : setattr(self, "_cell_type", val), None, """Cell type""")

class MotifFeature(Feature):
    """"""

    #binding_matrix = property(lambda self : getattr(self, "_binding_matrix"), None, None, """No documentation""")
    binding_matrix = property(lambda self : getattr(self, "_binding_matrix"), lambda self, val : setattr(self, "_binding_matrix", val), None, """No documentation""")

    #score = property(lambda self : getattr(self, "_score"), None, None, """No documentation""")
    score = property(lambda self : getattr(self, "_score"), lambda self, val : setattr(self, "_score", val), None, """No documentation""")

    #motif_feature_type = property(lambda self : getattr(self, "_motif_feature_type"), None, None, """No documentation""")
    motif_feature_type = property(lambda self : getattr(self, "_motif_feature_type"), lambda self, val : setattr(self, "_motif_feature_type", val), None, """No documentation""")

class RegulatoryFeature(FeatureWithID):
    """"""

    #description = property(lambda self : getattr(self, "_description"), None, None, """No documentation""")
    description = property(lambda self : getattr(self, "_description"), lambda self, val : setattr(self, "_description", val), None, """No documentation""")

    #bound_start = property(lambda self : getattr(self, "_bound_start"), None, None, """No documentation""")
    bound_start = property(lambda self : getattr(self, "_bound_start"), lambda self, val : setattr(self, "_bound_start", val), None, """No documentation""")

    #cell_type = property(lambda self : getattr(self, "_cell_type"), None, None, """No documentation""")
    cell_type = property(lambda self : getattr(self, "_cell_type"), lambda self, val : setattr(self, "_cell_type", val), None, """No documentation""")

    #bound_end = property(lambda self : getattr(self, "_bound_end"), None, None, """No documentation""")
    bound_end = property(lambda self : getattr(self, "_bound_end"), lambda self, val : setattr(self, "_bound_end", val), None, """No documentation""")

    #activity_evidence = property(lambda self : getattr(self, "_activity_evidence"), None, None, """No documentation""")
    activity_evidence = property(lambda self : getattr(self, "_activity_evidence"), lambda self, val : setattr(self, "_activity_evidence", val), None, """No documentation""")

class ConstrainedElementFeature(FeatureWithID):
    """"""

    #score = property(lambda self : getattr(self, "_score"), None, None, """No documentation""")
    score = property(lambda self : getattr(self, "_score"), lambda self, val : setattr(self, "_score", val), None, """No documentation""")

class VariationFeature(FeatureWithID):
    """"""

    #cell_type = property(lambda self : getattr(self, "_cell_type"), None, None, """No documentation""")
    cell_type = property(lambda self : getattr(self, "_cell_type"), lambda self, val : setattr(self, "_cell_type", val), None, """No documentation""")

    #alt_alleles = property(lambda self : getattr(self, "_alt_alleles"), None, None, """No documentation""")
    alt_alleles = property(lambda self : getattr(self, "_alt_alleles"), lambda self, val : setattr(self, "_alt_alleles", val), None, """No documentation""")

    #consequence_type = property(lambda self : getattr(self, "_consequence_type"), None, None, """No documentation""")
    consequence_type = property(lambda self : getattr(self, "_consequence_type"), lambda self, val : setattr(self, "_consequence_type", val), None, """No documentation""")

class StructuralVariationFeature(FeatureWithID):
    """"""

class MiscFeature(FeatureWithID):
    """"""

    #misc_set_code = property(lambda self : getattr(self, "_misc_set_code"), None, None, """No documentation""")
    misc_set_code = property(lambda self : getattr(self, "_misc_set_code"), lambda self, val : setattr(self, "_misc_set_code", val), None, """No documentation""")

    #clone_name = property(lambda self : getattr(self, "_clone_name"), None, None, """No documentation""")
    clone_name = property(lambda self : getattr(self, "_clone_name"), lambda self, val : setattr(self, "_clone_name", val), None, """No documentation""")

    #misc_set_name = property(lambda self : getattr(self, "_misc_set_name"), None, None, """No documentation""")
    misc_set_name = property(lambda self : getattr(self, "_misc_set_name"), lambda self, val : setattr(self, "_misc_set_name", val), None, """No documentation""")

    #type = property(lambda self : getattr(self, "_type"), None, None, """No documentation""")
    type = property(lambda self : getattr(self, "_type"), lambda self, val : setattr(self, "_type", val), None, """No documentation""")

    #name = property(lambda self : getattr(self, "_name"), None, None, """No documentation""")
    name = property(lambda self : getattr(self, "_name"), lambda self, val : setattr(self, "_name", val), None, """No documentation""")

    #state = property(lambda self : getattr(self, "_state"), None, None, """No documentation""")
    state = property(lambda self : getattr(self, "_state"), lambda self, val : setattr(self, "_state", val), None, """No documentation""")

class SimpleFeature(Feature):
    """"""

    #score = property(lambda self : getattr(self, "_score"), None, None, """No documentation""")
    score = property(lambda self : getattr(self, "_score"), lambda self, val : setattr(self, "_score", val), None, """No documentation""")

    #external_name = property(lambda self : getattr(self, "_external_name"), None, None, """No documentation""")
    external_name = property(lambda self : getattr(self, "_external_name"), lambda self, val : setattr(self, "_external_name", val), None, """No documentation""")

    #logic_name = property(lambda self : getattr(self, "_logic_name"), None, None, """No documentation""")
    logic_name = property(lambda self : getattr(self, "_logic_name"), lambda self, val : setattr(self, "_logic_name", val), None, """No documentation""")

class RepeatFeature(Feature):
    """"""

    #description = property(lambda self : getattr(self, "_description"), None, None, """No documentation""")
    description = property(lambda self : getattr(self, "_description"), lambda self, val : setattr(self, "_description", val), None, """No documentation""")

class CDSFeature(FeatureWithID):
    """"""

    #source = property(lambda self : getattr(self, "_source"), None, None, """No documentation""")
    source = property(lambda self : getattr(self, "_source"), lambda self, val : setattr(self, "_source", val), None, """No documentation""")

    #parent = property(lambda self : getattr(self, "_parent"), None, None, """No documentation""")
    parent = property(lambda self : getattr(self, "_parent"), lambda self, val : setattr(self, "_parent", val), None, """No documentation""")

    #phase = property(lambda self : getattr(self, "_phase"), None, None, """No documentation""")
    phase = property(lambda self : getattr(self, "_phase"), lambda self, val : setattr(self, "_phase", val), None, """No documentation""")

class Location(_pyrest_core.BaseObject):
    """"""

class CoordMapping(_pyrest_core.BaseObject):
    """"""

    #mapped = property(lambda self : getattr(self, "_mapped"), None, None, """No documentation""")
    mapped = property(lambda self : getattr(self, "_mapped"), lambda self, val : setattr(self, "_mapped", val), None, """No documentation""")

    #original = property(lambda self : getattr(self, "_original"), None, None, """No documentation""")
    original = property(lambda self : getattr(self, "_original"), lambda self, val : setattr(self, "_original", val), None, """No documentation""")

CoordMapping._construction_rules = {"mapped":Location, "original":Location}


__feature_types = {
        'gene' : GeneFeature,
        'transcript' : TranscriptFeature,
        'cds': CDSFeature,
        'exon' : ExonFeature,
        'repeat' : RepeatFeature,
        'simple' : SimpleFeature,
        'misc' : MiscFeature,
        'variation' : VariationFeature,
        'somatic_variation' : VariationFeature,
        'structural_variation' : StructuralVariationFeature,
        'somatic_structural_variation' : StructuralVariationFeature,
        'constrained' : ConstrainedElementFeature,
        'regulatory' : RegulatoryFeature,
        'motif' : MotifFeature,
        'chipseq' : ChipSeqFeature,

        'translation' : TranslationFeature,
}

def feature_wrapper(d, r):
    """
    Wrapper arround the various types of features.
    It automatically selects the appropriate type for the fetched features.
    """
    t = d.get('object_type')
    if t is None:
        t = d.get('feature_type')
    if t is None:
        print("Unable to find the type of", d)
        t = Feature
    else:
        t = t.lower()
        if t not in __feature_types:
            print("Unrecognized feature type:", t)
            t = Feature
        else:
            t = __feature_types[t]
    return t(d,r)



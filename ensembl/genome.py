
from . import _pyrest_core

class Identifier(_pyrest_core.BaseObject):
    """"""

class Sequence(_pyrest_core.BaseObject):
    """"""

class Feature(_pyrest_core.BaseObject):
    """"""

    seq_region_name = property(_pyrest_core.fget("_seq_region_name"), None, None, """Name of the chromosome, scaffold, etc the feature is on""")

    feature_type = property(_pyrest_core.fget("_feature_type"), None, None, """Type of this feature, usually redundant with the class itself (e.g. ExonFeature, TranscriptFeature, etc)""")

    start = property(_pyrest_core.fget("_start"), None, None, """Start coordinate""")

    end = property(_pyrest_core.fget("_end"), None, None, """End coordinate""")

    strand = property(_pyrest_core.fget("_strand"), None, None, """Strand""")

    assembly_name = property(_pyrest_core.fget("_assembly_name"), None, None, """Name of the genome assembly""")

class FeatureWithID(Feature):
    """"""

    id = property(_pyrest_core.fget("_id"), None, None, """No documentation""")

class ExonFeature(FeatureWithID):
    """"""

    source = property(_pyrest_core.fget("_source"), None, None, """No documentation""")

    constitutive = property(_pyrest_core.fget("_constitutive"), None, None, """No documentation""")

    ensembl_phase = property(_pyrest_core.fget("_ensembl_phase"), None, None, """No documentation""")

    ensembl_end_phase = property(_pyrest_core.fget("_ensembl_end_phase"), None, None, """No documentation""")

    parent = property(_pyrest_core.fget("_parent"), None, None, """No documentation""")

    version = property(_pyrest_core.fget("_version"), None, None, """No documentation""")

    rank = property(_pyrest_core.fget("_rank"), None, None, """No documentation""")

class TranslationFeature(FeatureWithID):
    """"""

    description = property(_pyrest_core.fget("_description"), None, None, """No documentation""")

    parent = property(_pyrest_core.fget("_parent"), None, None, """No documentation""")

    interpro = property(_pyrest_core.fget("_interpro"), None, None, """No documentation""")

    type = property(_pyrest_core.fget("_type"), None, None, """No documentation""")

class FeatureLikeBiotype(FeatureWithID):
    """"""

    biotype = property(_pyrest_core.fget("_biotype"), None, None, """No documentation""")

    external_name = property(_pyrest_core.fget("_external_name"), None, None, """No documentation""")

    description = property(_pyrest_core.fget("_description"), None, None, """No documentation""")

    source = property(_pyrest_core.fget("_source"), None, None, """No documentation""")

    version = property(_pyrest_core.fget("_version"), None, None, """No documentation""")

    logic_name = property(_pyrest_core.fget("_logic_name"), None, None, """No documentation""")

class TranscriptFeature(FeatureLikeBiotype):
    """"""

    translation = property(_pyrest_core.fget("_translation"), None, None, """No documentation""")

    exon = property(_pyrest_core.fget("_exon"), None, None, """No documentation""")

    parent = property(_pyrest_core.fget("_parent"), None, None, """No documentation""")

TranscriptFeature._construction_rules = {"exon":ExonFeature, "translation":TranslationFeature}

class GeneFeature(FeatureLikeBiotype):
    """"""

    transcript = property(_pyrest_core.fget("_transcript"), None, None, """No documentation""")

GeneFeature._construction_rules = {"transcript":TranscriptFeature}

class ChipSeqFeature(Feature):
    """"""

    chipseq_feature_type = property(_pyrest_core.fget("_chipseq_feature_type"), None, None, """ChipSeq type""")

    cell_type = property(_pyrest_core.fget("_cell_type"), None, None, """Cell type""")

class MotifFeature(Feature):
    """"""

    binding_matrix = property(_pyrest_core.fget("_binding_matrix"), None, None, """No documentation""")

    score = property(_pyrest_core.fget("_score"), None, None, """No documentation""")

    motif_feature_type = property(_pyrest_core.fget("_motif_feature_type"), None, None, """No documentation""")

class RegulatoryFeature(FeatureWithID):
    """"""

    description = property(_pyrest_core.fget("_description"), None, None, """No documentation""")

    bound_start = property(_pyrest_core.fget("_bound_start"), None, None, """No documentation""")

    cell_type = property(_pyrest_core.fget("_cell_type"), None, None, """No documentation""")

    bound_end = property(_pyrest_core.fget("_bound_end"), None, None, """No documentation""")

    activity_evidence = property(_pyrest_core.fget("_activity_evidence"), None, None, """No documentation""")

class ConstrainedElementFeature(FeatureWithID):
    """"""

    score = property(_pyrest_core.fget("_score"), None, None, """No documentation""")

class VariationFeature(FeatureWithID):
    """"""

    cell_type = property(_pyrest_core.fget("_cell_type"), None, None, """No documentation""")

    alt_alleles = property(_pyrest_core.fget("_alt_alleles"), None, None, """No documentation""")

    consequence_type = property(_pyrest_core.fget("_consequence_type"), None, None, """No documentation""")

class StructuralVariationFeature(FeatureWithID):
    """"""

class MiscFeature(FeatureWithID):
    """"""

    misc_set_code = property(_pyrest_core.fget("_misc_set_code"), None, None, """No documentation""")

    clone_name = property(_pyrest_core.fget("_clone_name"), None, None, """No documentation""")

    misc_set_name = property(_pyrest_core.fget("_misc_set_name"), None, None, """No documentation""")

    type = property(_pyrest_core.fget("_type"), None, None, """No documentation""")

    name = property(_pyrest_core.fget("_name"), None, None, """No documentation""")

    state = property(_pyrest_core.fget("_state"), None, None, """No documentation""")

class SimpleFeature(Feature):
    """"""

    score = property(_pyrest_core.fget("_score"), None, None, """No documentation""")

    external_name = property(_pyrest_core.fget("_external_name"), None, None, """No documentation""")

    logic_name = property(_pyrest_core.fget("_logic_name"), None, None, """No documentation""")

class RepeatFeature(Feature):
    """"""

    description = property(_pyrest_core.fget("_description"), None, None, """No documentation""")

class CDSFeature(FeatureWithID):
    """"""

    source = property(_pyrest_core.fget("_source"), None, None, """No documentation""")

    parent = property(_pyrest_core.fget("_parent"), None, None, """No documentation""")

    phase = property(_pyrest_core.fget("_phase"), None, None, """No documentation""")

class Location(_pyrest_core.BaseObject):
    """"""

class CoordMapping(_pyrest_core.BaseObject):
    """"""

    mapped = property(_pyrest_core.fget("_mapped"), None, None, """No documentation""")

    original = property(_pyrest_core.fget("_original"), None, None, """No documentation""")

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



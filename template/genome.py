
#__GENERATED_OBJECTS__

features = {
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

"""
    Wrapper arround the various types of features.
    It automatically selects the appropriate type for the fetched features.
"""
def feature_wrapper(d, r):
    t = d.get('object_type')
    if t is None:
        t = d.get('feature_type')
    if t is None:
        print("Unable to find the type of", d)
        t = Feature
    else:
        t = t.lower()
        if t not in features:
            print("Unrecognized feature type:", t)
            t = Feature
        else:
            t = features[t]
    return t(d,r)


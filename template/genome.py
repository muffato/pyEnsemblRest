
#__GENERATED_OBJECTS__

features = {
        'gene' : GeneFeature,
        'transcript' : TranscriptFeature,
        'translation' : TranslationFeature,
        'exon' : ExonFeature
}
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


from . import _pyrest_core

class Identifier(_pyrest_core.BaseObject):
    """"""

class Sequence(_pyrest_core.BaseObject):
    """"""

class Feature(_pyrest_core.BaseObject):
    """"""

class ExonFeature(Feature):
    """"""

class TranslationFeature(Feature):
    """"""

class TranscriptFeature(Feature):
    """"""

    #Translation = property(lambda self : getattr(self, "_Translation"), None, None, """None""")
    Translation = property(lambda self : getattr(self, "_Translation"), lambda self, val : setattr(self, "_Translation", val), None, """None""")

    #Exon = property(lambda self : getattr(self, "_Exon"), None, None, """None""")
    Exon = property(lambda self : getattr(self, "_Exon"), lambda self, val : setattr(self, "_Exon", val), None, """None""")

TranscriptFeature._construction_rules = {"Exon":ExonFeature, "Translation":TranslationFeature}

class GeneFeature(Feature):
    """"""

    #Transcript = property(lambda self : getattr(self, "_Transcript"), None, None, """None""")
    Transcript = property(lambda self : getattr(self, "_Transcript"), lambda self, val : setattr(self, "_Transcript", val), None, """None""")

GeneFeature._construction_rules = {"Transcript":TranscriptFeature}

class Location(_pyrest_core.BaseObject):
    """"""

class CoordMapping(_pyrest_core.BaseObject):
    """"""

    #mapped = property(lambda self : getattr(self, "_mapped"), None, None, """None""")
    mapped = property(lambda self : getattr(self, "_mapped"), lambda self, val : setattr(self, "_mapped", val), None, """None""")

    #original = property(lambda self : getattr(self, "_original"), None, None, """None""")
    original = property(lambda self : getattr(self, "_original"), lambda self, val : setattr(self, "_original", val), None, """None""")

CoordMapping._construction_rules = {"mapped":Location, "original":Location}


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



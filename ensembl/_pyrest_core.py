
import sys

def dict_wrapper(new_type):
    return lambda d, r : {k: new_type(v, r) for (k,v) in d.items()}

# Base class for JSON dictionnaries
# Each (key,value) is promoted to object attributes
# The constructor looks into <construction_rules> to use the correct type for each value

def fget(x):
    return lambda s : getattr(s, x)
def fset(x):
    return lambda s, v: setattr(s, x, v)

# New-style class
# Otherwise, all the instances share the same type "instance"
class BaseObject(object):

    def __init__(self, adict, rest_server):
        self._server = rest_server
        for k, v in adict.items():
            k = k.lower()
            new_class = None
            if (isinstance(v, dict)) or (isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict)):
                if k in self._construction_rules:
                    new_class = self._construction_rules[k]
                    #print("new system:", k, new_class)
                else:
                    # This test is only needed in development mode
                    print("No property type defined for '%s' in %s" % (k, type(self)), file=sys.stderr)
            vv = construct_object_from_json(v, new_class, rest_server)
            # k is for the property with documentation, kk is for the actual value
            kk = "_" + k
            if k not in dir(self):
                doc = "Undocumented attribute (guessed from the downloaded objects)"
                print("'%s' (in %s) has no documentation" % (k, type(self)), file=sys.stderr)
                setattr(type(self), k, property(fget(kk), fset(kk), None, doc))
            self.__dict__[kk] = vv

    # __repr__ defaults to something like '<ensembl.compara.NCBITaxon object at 0x7f85de15f668>'
    # __str__ shows the content of the object at its first level only (it calls __repr__ on the sub-objects, not __str__), e.g.
    #  "ensembl.compara.NCBITaxon(children=[<ensembl.compara.NCBITaxon object at 0x7f85de15fa20>, <ensembl.compara.NCBITaxon object at 0x7f85de15fac8>], tags={'scientific name': ['Homo sapiens'], 'name': ['Homo sapiens'], 'common name': ['man'], 'genbank common name': ['human'], 'authority': ['Homo sapiens Linnaeus, 1758'], 'ensembl alias name': ['Human']}, scientific_name='Homo sapiens', leaf=0, name='Homo sapiens', id='9606', parent=<ensembl.compara.NCBITaxon object at 0x7f85de15f6d8>)"
    def __str__(self):
        return self.__class__.__module__ + '.' + self.__class__.__name__ + '(' + ', '.join(x[1:] + '=' + repr(y) for (x,y) in self.__dict__.items() if x != '_server') + ')'

    server = property(fget('_server'), fset('_server'), None, 'REST server that was used to fetch this object')

def construct_object_from_json(obj, new_class, rest_server):
    if new_class is None:
        return obj
    if isinstance(obj, dict):
        return new_class(obj, rest_server)
    elif isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):
        return [new_class(_, rest_server) for _ in obj]
    else:
        return obj




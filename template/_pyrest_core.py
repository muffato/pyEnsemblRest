
import sys

# A dictionnary of (class, key): class
construction_rules = {}


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
        self.__set_new_field('server', rest_server, 'REST server that was used to fetch this object')
        for k, v in adict.items():
            # This test is only needed in development mode
            if ((self.__class__, k) not in construction_rules) and ((isinstance(v, dict)) or (isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict))):
                print("'%s' undefined for %s" % (k, type(self)), file=sys.stderr)
            new_class = construction_rules.get( (self.__class__, k) )
            vv = construct_object_from_json(v, new_class, rest_server)
            self.__set_new_field(k, vv)

    def __set_new_field(self, k, value, doc = None):
        # k is for the property with documentation, kk is for the actual value
        kk = "_" + k
        if k not in type(self).__dict__:
            if doc is None:
                doc = "Undocumented attribute (guessed from the downloaded objects)"
            setattr(type(self), k, property(fget(kk), fset(kk), None, doc))
        self.__dict__[kk] = value

    def __str__(self):
        return '{' + ',\n'.join(str(x) + ': ' + str(y) for (x,y) in self.__dict__.items()) + '}'


def construct_object_from_json(obj, new_class, rest_server):
    if new_class is None:
        return obj
    if isinstance(obj, dict):
        return new_class(obj, rest_server)
    elif isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):
        return [new_class(_, rest_server) for _ in obj]
    else:
        return obj



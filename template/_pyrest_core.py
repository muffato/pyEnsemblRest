
import sys

# A dictionnary of (class, key): class
construction_rules = {}


# Base class for JSON dictionnaries
# Each (key,value) is promoted to object attributes
# The constructor looks into <construction_rules> to use the correct type for each value

# New-style class
# Otherwise, all the instances share the same type "instance"
class BaseObject(object):

    def __init__(self, adict):
        self.__dict__.update(adict)
        for k, v in adict.items():
            new_class = construction_rules.get( (self.__class__, k))
            # This test is only needed in development mode
            if (new_class is None) and ((isinstance(v, dict)) or (isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict))):
                print("'%s' undefined for %s" % (k, type(self)), file=sys.stderr)
            self.__dict__[k] = construct_object_from_json(v, new_class)

    def __str__(self):
        return '{' + ',\n'.join(str(x) + ': ' + str(y) for (x,y) in self.__dict__.items()) + '}'


def construct_object_from_json(obj, new_class):
    if new_class is None:
        return obj
    if isinstance(obj, dict):
        return new_class(obj)
    elif isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):
        return [new_class(_) for _ in obj]
    else:
        return obj



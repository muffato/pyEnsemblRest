
import sys

construction_rules = {}

# New-style class
# Otherwise, all the instances share the same type "instance"
class BaseObject(object):

	def __init__(self, adict):
		self.__dict__.update(adict)
		for k, v in adict.items():
			new_class = construction_rules.get( (self.__class__, k), BaseObject)
			if isinstance(v, dict):
				self.__dict__[k] = new_class(v)
				if new_class == BaseObject:
					print("'%s' undefined for '%s'" % (k, type(self)), file=sys.stderr)
			elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
				self.__dict__[k] = [new_class(_) for _ in v]

	def __str__(self):
		return '{' + ',\n'.join(str(x) + ': ' + str(y) for (x,y) in self.__dict__.items()) + '}'



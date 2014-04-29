

import sys
import glob
import os.path
import xml.etree.ElementTree as ET

# Command-line arguments

config_root = ET.parse(sys.argv[1]).getroot()
rest_checkout = sys.argv[2]



# Will keep the content of all the files we're generating
files = {}

# The template modules that must be present
for module_name in ['_pyrest_core', '_pyrest_server', '__init__']:
	with open('template/%s.py' % module_name, 'r') as f:
		files[module_name] = f.read()

def replace_placeholder_in_template(filename, key, content_list, sep=''):
	files[filename] = files[filename].replace('#'+key, sep.join(content_list))


## Generate all the modules with basic object definition

template_init_import_module = 'import ensembl.%s'
template_module_header = 'import ensembl'

template_module_object = """
class %s(ensembl.BaseObject):
	\"\"\"%s\"\"\"
"""


init_imports = []

# All the module names
for config_python_module in config_root.find('objects'):
	module_name = config_python_module.get('name')
	init_imports.append(template_init_import_module % module_name)

	# All the objects in this module
	files[module_name] = template_module_header + "\n" + "".join(
		template_module_object % (config_python_object.get('name'), config_python_object.get('description', '')) for config_python_object in config_python_module
	)

	# Adds the extra methods we want on those objects
	filename = 'template/%s.py' % module_name
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			files[module_name] = files[module_name] + f.read()

replace_placeholder_in_template('__init__', '__MODULE_IMPORTS__', init_imports, sep='\n')



endpoints = {}
for f in glob.glob('%s/root/documentation/*.conf' % rest_checkout):
	for e in ET.parse(f).getroot():
		endpoints[e.tag] = e

# Decodes a text that is a bunch of "key=value" lines
# The keys listed in "mul" can be found in several copies
def decode_config(t, mul=[]):
	l = [tuple(_.strip() for _ in l.split('=')) for l in t.splitlines() if '=' in l]
	d = dict(l)
	for k in mul:
		if k in d:
			d[k] = [x[1] for x in l if x[0] == k]
	return d


template_endpoint = """
	def {1}(self, {2}, **kwargs):
		\"\"\"{0}\"\"\"
		return self.build_rest_answer({4}, {5}, '{3}'.format({2}), kwargs)
"""



endpoint_code = []
for e in config_root.find('endpoints'):

	re = endpoints[e.get('id')]
	d = decode_config(re.text, ['output'])

	parameters = dict((p.tag, decode_config(p.text)) for p in re.find('params'))
	d['endpoint'] = d['endpoint'].replace('"', '')


	doc_params = '\n\nRequired parameters:\n'
	endpoint_args = []
	required_params = []
	for x in d['endpoint'].split('/'):
		if x.startswith(':'):
			endpoint_args.append('{%d}' % len(required_params))
			p = x[1:]
			dp = parameters[p]
			doc_params = doc_params + "- %s (%s)\n\t%s\n" % (p, dp['type'], dp['description'])
			required_params.append(p)
		else:
			endpoint_args.append(x)

	doc_params = doc_params + '\nOptional parameters:\n'
	for (p,dp) in parameters.items():
		if p in required_params:
			continue
		if 'deprecated' in dp:
			continue
		doc_params = doc_params + "- %s (%s)\n\t%s\n" % (p, dp['type'], dp['description'])

	doc = [
		d['description'] + "\n",
		('Return type', 'ensembl.' + e.get('object')),
		('Valid formats', ", ".join(d['output'])),
		('HTTP endpoint', d['endpoint'])
	]
	doc_string = "\n".join("%s: %s" % x if isinstance(x, tuple) else x for x in doc) + doc_params
	endpoint_code.append( template_endpoint.format(doc_string, e.get('name'), ", ".join(required_params), '/'.join(endpoint_args), "ensembl."+e.get('object'), d['output']) )

replace_placeholder_in_template('_pyrest_server', '__ENDPOINTS_METHODS__', endpoint_code, sep="\n")


## Read all the other configurations and update _pyrest_server
def build_and_replace(template_anchor, config_tag_name, expected_tag_name, callback, sep=",\n"):
	config_all_rate_limiters = []
	for config_entry in config_root.find(config_tag_name):
		assert config_entry.tag == expected_tag_name
		config_all_rate_limiters.append( callback(config_entry) )
	replace_placeholder_in_template('_pyrest_server', template_anchor, config_all_rate_limiters, sep=sep)

# construction_rules
build_and_replace('__CONSTRUCTION_RULES__', 'object_links', 'link',
		lambda c: "ensembl._pyrest_core.construction_rules[(ensembl.%s,'%s')] = ensembl.%s" % (c.get('src'), c.get('key'), c.get('target')), sep="\n"
)

# content_types
build_and_replace('__CONTENT_TYPES__', 'content_types', 'content_type',
		lambda c: '"%s": "%s"' % (c.get('alias'), c.get('mime'))
)

# response codes
build_and_replace('__RESPONSE_CODES__', 'response_codes', 'response_code',
		lambda c: '%s: ("%s", "%s")' % (c.get('code'), c.get('title'), c.get('description'))
)

# rate limiters
build_and_replace('__RATE_LIMITERS__', 'rate_limiters', 'rate_limiter',
		lambda c: '%s: collections.deque([], %s-1)' % (c.get('period'), c.get('max_requests'))
)


## Write down all the files to the disk

for (filename,content) in files.items():
	with open('ensembl/%s.py' % filename, 'w') as f:
		print(content, file=f)




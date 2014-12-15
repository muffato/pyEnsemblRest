

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

template_property = """
    #{0} = property(lambda self : getattr(self, "_{0}"), None, None, \"\"\"{1}\"\"\")
    {0} = property(lambda self : getattr(self, "_{0}"), lambda self, val : setattr(self, "_{0}", val), None, \"\"\"{1}\"\"\")
"""

init_imports = []

# All the module names
for config_python_module in config_root.find('objects'):
    # config_python_module is a <namespace> element
    module_name = config_python_module.get('name')
    if module_name is None:
        raise SyntaxError("Namespace without a name")
    init_imports.append(template_init_import_module % module_name)

    # All the objects in this module
    module_code = [ template_module_header, "\n" ]
    for config_python_object in config_python_module:
        # config_python_object is a <object> element
        module_code.append( template_module_object % (config_python_object.get('name'), config_python_object.get('description', '')) )
        for prop in config_python_object:
            # prop is a <property> element
            module_code.append( template_property.format( prop.get('name'), prop.get('description') ) )
    files[module_name] = "".join(module_code)

    # Adds the extra methods we want on those objects
    filename = 'template/%s.py' % module_name
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            files[module_name] = files[module_name] + f.read()

replace_placeholder_in_template('__init__', '__MODULE_IMPORTS__', init_imports, sep='\n')



endpoints = {}
for f in glob.glob('%s/root/documentation/*.conf' % rest_checkout):
    try:
        for e in ET.parse(f).getroot():
            endpoints[e.tag] = e
    except ET.ParseError as ex:
        raise SyntaxError("Cannot parse " + f) from ex

# Decodes a text that is a bunch of "key=value" lines
# The keys listed in "mul" can be found in several copies
def decode_config(t, mul=[]):
    pairs = []
    for l in t.splitlines():
        part = l.partition('=')
        if part[1] == '=':
            pairs.append( (part[0].strip(), part[2].strip()) )
    #l = [tuple(_.strip() for _ in l.partition('=')) for l in t.splitlines() if '=' in l]
    d = dict(pairs)
    for k in mul:
        if k in d:
            d[k] = [x[1] for x in pairs if x[0] == k]
    return d


template_endpoint = '''
    def {0}(self, {1}, **kwargs):
        """{3}

Return type: {4}
Valid formats: {6}
HTTP endpoint: {7}

{8}
{9}"""
        return self.build_rest_answer({4}, {5}, {10}, {11}, '{2}'.format({1}), kwargs)
'''

template_endpoint_no_args = '''
    def {0}(self, **kwargs):
        """{3}

Return type: {4}
Valid formats: {6}
HTTP endpoint: {7}

{8}
{9}"""
        return self.build_rest_answer({4}, {5}, {10}, {11}, '{2}', kwargs)
'''



def parameter_docstring(param_name, parameter_details):
    return "- %s (%s)\n    %s\n" % (param_name, parameter_details['type'], parameter_details['description'])


def allparams_docstring(title, allparams, parameter_details):
    if len(allparams) == 0:
        return ''
    return ('%s:\n' % title) + "".join(parameter_docstring(p, parameter_details[p]) for p in allparams)


def get_code_for_endpoint(e):

    re = endpoints[e.get('id')]
    d = decode_config(re.text, ['output'])
    try:
        d['endpoint'] = d['endpoint'].replace('"', '')
    except KeyError:
        raise SyntaxError("No 'endpoint' parameter in the endpoint id '{0}'".format(re.tag))

    ordered_parameters = []
    for p in (re.find('params') or []):
        t = p.text
        if list(p):
            print("Warning, there are some HTML tags inside the description of '{0}'. Trying to sort it out ...".format(d['endpoint']), file=sys.stderr)
            for x in p:
                t = t + ET.tostring(x, encoding="unicode", method="html")
            print("Please check the reconstructed string:", t, file=sys.stderr )
        ordered_parameters.append( (p.tag,decode_config(t)) )
    parameter_details = dict(ordered_parameters)

    endpoint_url_segments = []
    required_params = []
    for url_segment in d['endpoint'].split('/'):
        if url_segment.startswith(':'):
            endpoint_url_segments.append('{%d}' % len(required_params))
            p = url_segment[1:]
            dp = parameter_details[p]
            required_params.append(p)
            if dp.get('required') != '1':
                print("'required' should be set to 1 for '%s' in '%s'" % (p, d['endpoint']), file=sys.stderr)
        else:
            endpoint_url_segments.append(url_segment)

    optional_params = [p for (p,dp) in ordered_parameters if (p not in required_params) and ('deprecated' not in dp)]

    return (template_endpoint if len(required_params) else template_endpoint_no_args).format(
        e.get('name'),
        ", ".join(required_params),
        '/'.join(endpoint_url_segments),
        d['description'],
        "ensembl." + e.get('object') if e.get('object') is not None else "None",
        d['output'],
        ", ".join(d['output']),
        d['endpoint'],
        allparams_docstring('Required parameters', required_params, parameter_details),
        allparams_docstring('Optional parameters', optional_params, parameter_details),
        optional_params,
        None if e.get('accessor') is None else '"%s"' % e.get('accessor')
    )


## Read all the other configurations and update _pyrest_server
def build_and_replace(template_anchor, config_tag_name, expected_tag_name, callback, sep=",\n"):
    config_all_rate_limiters = []
    for config_entry in config_root.find(config_tag_name):
        assert config_entry.tag == expected_tag_name
        config_all_rate_limiters.append( callback(config_entry) )
    replace_placeholder_in_template('_pyrest_server', template_anchor, config_all_rate_limiters, sep=sep)



# endpoint accessors
build_and_replace('__ENDPOINTS_METHODS__', 'endpoints', 'endpoint', get_code_for_endpoint, sep="\n")

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




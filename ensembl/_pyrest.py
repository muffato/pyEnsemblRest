
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
					print k
			elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
				self.__dict__[k] = [new_class(_) for _ in v]

	def __str__(self):
		return '{' + ',\n'.join(str(x) + ': ' + str(y) for (x,y) in self.__dict__.items()) + '}'



import httplib2
import json
import time
import collections

endpoint_2_class = {}

content_types = {
	'json' : 'application/json',
	'nh' : 'text/x-nh',
	'newick' : 'text/x-nh'
}

class RestServer:

	# the key is the time interval (in seconds)
	# the list stores the last x attempts
	last_requests = {
		1: collections.deque([], 6-1),
		3600: collections.deque([], 11100-1)
	}

	def __init__(self, server_url = None):
		if server_url is None:
			server_url = "http://beta.rest.ensembl.org"
		self.server_url = server_url
		self.http = httplib2.Http(".cache")


	def get_json_answer(self, url, content_type=None):

		# Rate limiter
		for (i,l) in self.last_requests.iteritems():
			if len(l) == l.maxlen:
				curr_time = time.time()
				oldest_time = l[0]
				if curr_time-oldest_time < i:
					print "sleep (%d)" % i, i - (curr_time-oldest_time)
					time.sleep(i - (curr_time-oldest_time))

		curr_time = time.time()
		for (i,l) in self.last_requests.iteritems():
			l.append(time.time())
			while l[0] < curr_time-i:
				print "clear", i
				l.popleft()
		print self.last_requests
		print content_type
		resp, content = self.http.request(self.server_url+url, method="GET", headers={"Content-Type":content_type})

		if not resp.status == 200:
			raise httplib2.HttpLib2Error( "Invalid response: %d" % resp.status )

		return content


	def build_rest_answer(self, endpoint, args, kwargs={}):
		format = kwargs.get('format')
		if format is not None:
			format = format.lower()
			if format not in content_types:
				print "unrecognzied format", format
				format = None
		content = self.get_json_answer(endpoint + args, content_types.get(format, content_types['json']))

		print "Format", format
		if format is not None:
			return content

		j = json.loads(content)
		c = endpoint_2_class[endpoint]
		return c(j)

	def getGeneTreeById(self, stable_id, **kwargs):
		return self.build_rest_answer('/genetree/id/', stable_id, kwargs)

	def getGeneTreeByMemberId(self, stable_id):
		return self.build_rest_answer('/genetree/member/id/', stable_id)

	def getGeneTreeByMemberSymbol(self, species, symbol):
		return self.build_rest_answer('/genetree/member/symbol/', '%s/%s' % (species, symbol))

	def getAssemblyInfo(self, species):
		return self.build_rest_answer('/assembly/info/', species)

	def getAssemblyInfoRegion(self, species, region_name):
		return self.build_rest_answer('/assembly/info/', '%s/%s' % (species,region_name) )

	def getArchiveEntry(self, stable_id):
		return self.build_rest_answer('/archive/id/', stable_id)




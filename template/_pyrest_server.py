
import collections
import httplib2
import json
import time

import ensembl

content_types = {
#__CONTENT_TYPES__
}

return_codes = {
#__RESPONSE_CODES__
}

class RestServer:

	# the key is the time interval (in seconds)
	# the list stores the last x attempts
	last_requests = {
#__RATE_LIMITERS__
	}

	def __init__(self, server_url):
		self.server_url = server_url
		self.http = httplib2.Http(".cache")


	def get_json_answer(self, url, content_type=None):

		# Rate limiter
		for (i,l) in self.last_requests.items():
			if len(l) == l.maxlen:
				curr_time = time.time()
				oldest_time = l[0]
				if curr_time-oldest_time < i:
					#print "sleep (%d)" % i, i - (curr_time-oldest_time)
					time.sleep(i - (curr_time-oldest_time))

		curr_time = time.time()
		for (i,l) in self.last_requests.items():
			l.append(time.time())
			while l[0] < curr_time-i:
				#print "clear", i
				l.popleft()
		#print self.last_requests
		#print content_type
		print("getting "+self.server_url+"/"+url+" with the content_type:"+content_type)
		resp, content = self.http.request(self.server_url+"/"+url, method="GET", headers={"Content-Type":content_type})

		if resp.status not in return_codes:
			raise httplib2.HttpLib2Error( "Unknown response code: %d\n%s" % (resp.status, resp) )
		if return_codes[resp.status][0] != "OK":
			raise httplib2.HttpLib2Error( "Invalid response code: %s (%d)\n%s\n%s" % (return_codes[resp.status][0], resp.status, return_codes[resp.status][1], resp) )

		return content.decode('utf-8')


	def build_rest_answer(self, new_object, allowed_formats, url, kwargs={}):

		format = kwargs.pop('format', None)
		if format is not None:
			format = format.lower()
			if format not in allowed_formats:
				#print "unrecognzied format", format
				format = None

		if len(kwargs):
			url = url + "?" + "&".join("%s=%s" % _ for _ in kwargs.items())

		content = self.get_json_answer(url, content_types.get(format, content_types['json']))

		#print "Format", format
		if format is not None:
			return content

		return new_object(json.loads(content))

#__ENDPOINTS_METHODS__


#__CONSTRUCTION_RULES__

EnsemblRestServer = RestServer(server_url = "http://beta.rest.ensembl.org")
EnsemblGenomesRestServer = RestServer(server_url = "http://test.rest.ensemblgenomes.org")




import collections
import httplib2
import math
import json
import time
import urllib
import sys

# This imports all the public packages (the ones that don't start with an underscore) and the content of __all__
from . import *
# So we need to add _pyrest_core
from . import _pyrest_core

class RestServerException(Exception):
    """Used when the server returned a non-OK code"""
    pass

class UnknownResponseCodeException(RestServerException):
    """Used when the RestServer does not know the meaning of the HTTP response code returned by the server"""
    pass
class NotOKResponseCodeException(RestServerException):
    """Used when the server returned the response code of an error"""
    pass

class UnavailableFormatException(RestServerException):
    """Used when the required output format is not available for this endpoint"""
    pass

class RestServer:
    """
    RestServer is a class that knows how to communicate with the Ensembl REST servers.
    """


    __content_types = {
    #__CONTENT_TYPES__
    }

    __return_codes = {
    #__RESPONSE_CODES__
    }

    def __init__(self, server_url):
        """
        Constructor for the RestServer class.
        server_url is the URL of the server.
        """
        self.server_url = server_url
        self.http = httplib2.Http()
        self.last_headers = None


    def __get_json_answer(self, url, content_type=None):

        # Rate limiter
        if self.last_headers is not None:
            time_remaining = int(self.last_headers['x-ratelimit-reset'])
            requests_remaining = int(self.last_headers['x-ratelimit-remaining'])
            t = time_remaining * math.exp( -requests_remaining / time_remaining )
            if t > .001:
                print("sleeping", t, "seconds before calling", self.server_url)
                time.sleep(t)

        #print("getting "+self.server_url+"/"+url+" with the content_type:"+content_type)
        while True:
            resp, content = self.http.request(self.server_url+"/"+url, method="GET", headers={"Content-Type":content_type})
            if resp.status == 429:
                print(self.server_url, "asked to wait", resp['retry-after'], "seconds", file=sys.stderr)
                time.sleep(float(resp['retry-after']))
            else:
                break

        if resp.status not in self.__return_codes:
            raise UnknownResponseCodeException(resp.status, resp, content)
        if self.__return_codes[resp.status][0] != "OK":
            raise NotOKResponseCodeException(self.__return_codes[resp.status], resp.status, resp, content )
        self.last_headers = resp

        return content.decode('utf-8')


    def __build_rest_answer(self, new_object, allowed_formats, optional_params, accessor, url, kwargs={}):

        format = kwargs.pop('output_format', None)
        if format is not None:
            format = format.lower()
            if format not in allowed_formats:
                raise UnavailableFormatException(format)
                format = None

        if len(kwargs):
            ps = set(kwargs).intersection(optional_params)
            pairs = []
            for p in ps:
                vv = kwargs[p]
                if isinstance(vv, list):
                    pairs.extend( (p,_) for _ in vv)
                else:
                    pairs.append( (p,vv) )
            url = url + "?" + "&".join("%s=%s" % (p,urllib.parse.quote(str(v))) for (p,v) in pairs)

        content = self.__get_json_answer(url, self.__content_types.get(format, self.__content_types['json']))

        #print "Format", format
        if format is not None:
            return content

        j = json.loads(content)
        if accessor is not None:
            j = j[accessor]
        return _pyrest_core.construct_object_from_json(j, new_object, self)

#__ENDPOINTS_METHODS__



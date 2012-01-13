#coding: utf8

import oauth2 as oauth
import time
import urllib
import urllib2
import base64
try:
    import json
except:
    import simplejson as json

from urls import *
from method_missing import MethodMissing


class TwitterError(Exception):
    pass

CONVERT = lambda x: json.loads(x)
NOT_CONVERT = lambda x: x
REQUEST_METHODS = set(['GET', 'POST', 'PUT', 'DELETE'])

class Auth(object):
    def generate_request(self, url, method, params):
        raise NotImplementedError()
    
    def choose_method(self, url, method, params):
        if method == 'GET':
            request = urllib2.Request('%s?%s' % (url, urllib.urlencode(params)))
        else:
            request = urllib2.Request(url, data=urllib.urlencode(params))
            if method in REQUEST_METHODS:
                request.get_method = lambda: method
            else:
                raise TwitterError('There is not the method called %s' % method)
        return request
        
class NoAuth(Auth):
    def generate_request(self, url, method, params):
        return self.choose_method(url, method, params)

class BasicAuth(Auth):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def generate_request(self, url, method, params):
        request = self.choose_method(url, method, params)
        basic = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        request.add_header('Authorization', 'Basic %s' % basic)
        return request

class OAuth(Auth):
    def __init__(self, consumer_key, consumer_secret, token_key=None, token_secret=None):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        if token_key is not None and token_secret is not None:
            self.token = oauth.Token(token_key, token_secret)
    
    def generate_request(self, url, method, params):
        oauth_params = {
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_token': self.token.key,
            'oauth_consumer_key': self.consumer.key,
        }
        oauth_params.update(params)
        oauth_request = oauth.Request(method=method, url=url, parameters=oauth_params)
        oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        request = self.choose_method(url, method, params)
        request.add_header('Authorization', oauth_request.to_header()['Authorization'])
        return request

class Api(MethodMissing):
    def __init__(self, auth=None, convert_to_dict=True):
        self._auth = auth or NoAuth()
        self.convert = CONVERT if convert_to_dict else NOT_CONVERT
    
    def method_missing(self, name, *args, **kw):
        if name.endswith('stream'):
	    url = 'https://stream.twitter.com/1/statuses/' + name.split('_')[0] + '.json'
	    return self.stream(url, 'GET', **kw)
	if 'POST' in args:
	    method = 'POST'
	elif 'PUT' in args:
	    method = 'PUT'
        elif 'DELETE' in args:
            method = 'DELETE'
	elif kw.has_key('method'):
	    method = kw['method']
	    del kw['method']
	else:
	    method = 'GET'
	url = 'https://api.twitter.com/1/' + name.replace('__','/') + '.json'
	return self.fetch(url, method, **kw)

    def raw_response(self, url, method, **params):
        return urllib2.urlopen(self._auth.generate_request(url, method, params))
    
    def fetch(self, url, method, **params):
        return self.convert(self.raw_response(url, method, **params).read())
    
    def get(self, url, **params):
        return self.fetch(url, 'GET', **params)
    
    def post(self, url, **params):
        return self.fetch(url, 'POST', **params)
    
    def put(self, url, **params):
        return self.fetch(url, 'PUT', **params)
    
    def delete(self, url, **params):
        return self.fetch(url, 'DELETE', **params)
    
    def stream(self, url, method, **params):
        res = self.raw_response(url, method, **params)
        for line in res:
            yield self.convert(line)
    
    def user_stream(self, **params):
        return self.stream(STREAM_USER, 'GET', **params)
    

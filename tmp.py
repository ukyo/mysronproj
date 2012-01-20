#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup as BS
from config import *
import urllib
import urllib2

url="http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder"
def read(q):
    if type(q).__name__ == "unicode":
        q = q.encode("utf8")
    return urllib2.urlopen(url+"?appid="+yid+"&query="+q)

#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup as BS
from config import *
import urllib
import urllib2
import UserModelFactory
import json
import pldautils
import json
from EventTweetFactory import EventTweetFactory
import EventTweetRecommender



#url="http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder"
#def read(q):
#    if type(q).__name__ == "unicode":
#        q = q.encode("utf8")
#    return urllib2.urlopen(url+"?appid="+yid+"&query="+q)


#words = json.loads(open("backup", "r").read())
#fy = UserModelFactory.UserModelFactory(wordfile)
#bow = fy.formatter.format(words)

fty = EventTweetFactory(wordfile)
#recent = json.loads(open("recenteventtweets.json").read())

fy = UserModelFactory.UserModelFactory(wordfile)
f = open("log_murasaki8823.json", "r")
log = []
[log.extend(json.loads(a)["users"]) for a in f]
profs = []
[profs.extend(fy.parser.parse(l["description"])) for l in log]
bow = fy.formatter.format(profs)
ret = pldautils.get_topic_from_server_p(bow)
mizu = {"topic": ret}
f = open("eventtweetmodels_mixed2.json")
eventtweetmodels = [json.loads(l) for l in f]
recommender = EventTweetRecommender.EventTweetRecommender(eventtweetmodels)
#tweets = recommender.calc(json.load("mizumodel.json"), 30)
tweets = recommender.calc(mizu, 30)
tweets2 = recommender.calc(mizu, 30, "pro")
tokens = [t["event_info"]["tokens"] for t in tweets]
for t in tokens:
    print ' '.join(tt["word"] for tt in t)
f.close()
f = open("eventtweetmodels_mixed.json", "r")
i = 0
for l in f:
    print json.loads(l)["text"]
    i += 1
    if i > 30: break


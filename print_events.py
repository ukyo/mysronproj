#!/usr/bin/env python
#coding: utf8

from tinytwitter.tinytwitter import *
import config
import datetime
from twitter_params import *

api = Api(config.oauth)
rt = "%20-rt"

def pp(r):
    for t in r['results']:
        print t['text'].encode("utf8").replace("\n", "")
    

def loop():
    day = datetime.datetime.today()

    for i in range(3):
        r = api.search(q=dfd(day, 5)+event_jp+rt,
                       rpp="100",
                       page="1",
                       lang="ja",
                       result_type="recent")
        pp(r)
        time.sleep(3)
        r = api.search(q=dfd(day, 5)+event_jp+rt,
                       rpp="100",
                       page="2",
                       lang="ja",
                       result_type="recent")
        pp(r)
        time.sleep(3)
        r = api.search(q=dfdj(day, 5)+event_jp+rt,
                       rpp="100",
                       page="1",
                       lang="ja",
                       result_type="recent")
        pp(r)
        time.sleep(3)
        r = api.search(q=dfdj(day, 5)+event_jp+rt,
                       rpp="100",
                       page="2",
                       lang="ja",
                       result_type="recent")
        pp(r)
        time.sleep(3)
        day += datetime.timedelta(5)

loop()
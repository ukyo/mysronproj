#!/usr/bin/env python
#coding: utf8

import sys
import pytc
import twitter_params as tp
from tinytwitter import tinytwitter as tw
import time
import os
import MeCabParser
import datetime
from config import *
import json

api = tw.Api(oauth)

def read(x, n, result_type):
    """x日後からx+n日後のイベント情報が含まれるtweetを取得"""
    day_from = datetime.datetime.today() + datetime.timedelta(1)
    tweets = []
    rt = "%20-rt"
    
    def get(query):
        today = datetime.datetime.today()
        for i in range(1, 15):
            try:
                r = api.search(q=query,
                               page=i,
                               rpp="100",
                               lang="ja",
                               result_type=result_type)
                tweets.extend(r["results"])
            except:
                pass
    
    #mm/ddスタイルのイベントtweetの取得
    query = tp.event_jp + "%20" + tp.dfd(day_from, n) + rt
    get(query)
    
    #mm月dd日スタイルのイベントtweetの取得
    query = tp.event_jp + "%20" + tp.dfdj(day_from, n) + rt
    get(query)
    
    return tweets


def read_recent(x, n):
    return read(x, n, "recent")

def read_popular(x, n):
    return read(x, n, "popular")

if __name__ == '__main__':
    tweets = read_recent(1, 1)
    print json.dumps(tweets)
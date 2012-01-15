#!/usr/bin/env python
#coding: utf8

import sys
import pytc
import twitter_params as tp
from tinytwitter import tinytwitter as tw
import time
import tinytwitter
import os
import MeCabParser
import datetime
from config import *
import json

class Parser(MeCabParser.Parser):
    def parse(self, s, to_unicode=False):
        if type(s) == str:
            s = s.decode(self.encoding)
        s = self.normalizer.normalize(s).encode(self.encoding)
        node = self.tagger.parseToNode(s)
        ret = []
        while node:
            surface = node.surface
            if surface != "" and "名詞" in node.feature and not "名詞,数" in node.feature and not "非自立" in node.feature:
                if to_unicode:
                    surface = surface.decode(self.encoding)
                ret.append(surface)
            node = node.next
        return ret

class AbstractDBWriter(object):
    def write(self, s):
        pass
    
    def close(self):
        pass
    

class TCDBWriter(AbstractDBWriter):
    def __init__(self, dbname):
        self.db = pytc.HDB(dbname, pytc.HDBOWRITER | pytc.HDBOCREAT)
    
    def write(self, s):
        raise NotImplementedError

    def close(self):
        self.db.close()


class CountDBWriter(TCDBWriter):
    def write(self, s):
        self.db.addint(s, 1)

class FileWriter(AbstractDBWriter):
    def __init__(self, filename, nl=True):
        self.f = open(filename, "w")
        self.nl = "\n" if nl else ""
    
    def write(self, s):
        print s
        self.f.write(s)
        self.f.write(nl)
        self.f.flush()
    
    def close(self):
        self.f.close()


def read(start_day=0, per_iter=10, iteration=5, writer=AbstractDBWriter()):
    day = datetime.datetime.today() + datetime.timedelta(start_day)
    api = tw.Api(tw.OAuth(ck, cs, tk, ts))
    rt = "%20-rt"
    for i in range(1, iteration):
        try:
            q = tp.days_from_day_jp(day, i * per_iter)+rt
            for j in range(1,15):
                r = api.search(q=q, rpp="100", page=str(j), lang="ja")
                for k in r['results']:
                    tokens = parser.parse(k['text'])
                    for token in tokens:
                        print token
                        writer.write(token)
            day = day + datetime.timedelta(i * per_iter)
        except e:
            print e
            time.sleep(10)
    writer.close()

def read_text(start_day=0, per_iter=10, iteration=5, jp=False, writer=AbstractDBWriter()):
    day = datetime.datetime.today() + datetime.timedelta(start_day)
    api = tw.Api(oauth)
    rt = "%20-rt"
    day_fn = tp.dfdj if jp else tp.dfd
    for i in range(1, iteration):
        try:
            q = day_fn(day, per_iter)+rt+"%20"+tp.event_jp
            for j in range(1,5):
                r = api.search(q=q, rpp="100", page=str(j), lang="ja", response_type="recent")
                for k in r['results']:
                    print k['text']
                #for k in r['results']:
                #    writer.write(k['text'].encode('utf8'))
            day = day + datetime.timedelta(per_iter)
        except:
            time.sleep(3)
    writer.close()

def read_slow(start=0, n=10, jp=False, filename="hoge"):
    api = tw.Api(tw.OAuth(ck, cs, tk, ts))
    rt = "%20-rt"
    day_fn = tp.dfdj if jp else tp.dfd
    writer = FileWriter(filename)
    while 1:
        day = datetime.datetime.today() + datetime.timedelta(start)
        since_id = '0'
        res = api.search(q=day_fn(day, n)+"%20"+tp.event_jp+rt,
                        rpp="100",
                        since_id=since_id,
                        result_type="recent")
        since_id = res['mac_id_str']
        results = res['results']
        for r in results:
            writer.write(json.dumps(r))
        time.sleep(10)
        
if __name__ == '__main__':
    parser = Parser()
    start_day, per_iter, iteration, jp = map(int, sys.argv[1:5])
    read_text(start_day, per_iter, iteration, jp)

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
        
parser = Parser()
#reload(sys)
#sys.setdefaultencoding('utf-8')

db = pytc.HDB(sys.argv[1]+'.db', pytc.HDBOWRITER | pytc.HDBOCREAT)
day = datetime.datetime.today() + datetime.timedelta(int(sys.argv[2]))
api = tw.Api(tw.OAuth(ck, cs, tk, ts))
rt = "%20-rt"
for i in range(1, int(sys.argv[3])):
    try:
        q = tp.days_from_day_jp(day, i * 5)+rt
        for j in range(1,15):
            r = api.search(q=q, rpp="100", page=str(j), lang="ja")
            for k in r['results']:
                tokens = parser.parse(k['text'])
                for token in tokens:
                    print token
                    db.addint(token, 1)
        day = day + datetime.timedelta(i * 5)
    except:
        time.sleep(10)


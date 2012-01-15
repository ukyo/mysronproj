#coding: utf8

from tinytwitter.tinytwitter import *
import json
import sys
import os
import time
import re

nl_p = re.compile('\n')
u, p, o = sys.argv[1:4]
if len(sys.argv) > 4:
    proxy = sys.argv[4]
else:
    proxy = ""

os.environ["http_proxy"] = proxy
api = Api(BasicAuth(u, p), False)

f = open(o, 'w')
while 1:
    for t in api.sample_stream():
        try:
            d = json.loads(t)
            if d['user']['lang'] == 'ja':
                f.write(nl_p.sub('', d['text']).encode('utf8'))
                print d['text']
                f.write('\n')
                f.flush()
            elif t == '\n':
                break 
        except:
            pass
    time.sleep(240)
f.close()

#!/usr/bin/env python

import time
from tinytwitter import tinytwitter as tw
import sys
import json
import MeCabParser
import re

p_url = re.compile('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)')
p_hash = re.compile('#')
p_reply = re.compile('@[a-zA-Z0-9]+')
def normalize(s):
    s = p_url.sub('', s)
    s = p_hash.sub('', s)
    s = p_reply.sub('', s)
    return s

def main():
    u, p = sys.argv[1:3]
    f = open(str(time.time()), 'w')
    parser = MeCabParser.Parser()
    api = tw.Api(tw.BasicAuth(u, p))
    for t in api.sample_stream():
        try:
            if t['user']['lang'] == 'ja':
                t['parse_text'] = parser.parse(normalize(t['text']))
                f.write(json.dumps(t) + '\n')
                f.flush()
                print ','.join(t['parse_text'])
        except:
            pass

if __name__ == '__main__':
    main()
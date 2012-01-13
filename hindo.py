#!/usr/bin/env python

import pytc
import sys

db = pytc.HDB(sys.argv[1], pytc.HDBOWRITER|pytc.HDBOCREAT)
l = db.items()
d = {}

for item in l:
    d[item[0]] = db.addint(item[0], 0)

for k, v in sorted(d.items(), key=lambda x:x[1]):
    print k, v
db.close()
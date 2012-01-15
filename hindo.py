#!/usr/bin/env python

import pytc
import sys
from hizukereader import Parser
import re

split = re.compile(",").split

def flatten(input, output):
    i = open(input, "r")
    o = open(output, "w")
    parser = Parser()
    wl = parser.parse(i.readline().rstrip("\n"))
    for line in i:
        if "[[" in line.rstrip("\n"):
            o.write("\n")
        else:
            o.write(",")
        wl = parser.parse(line)
        o.write(','.join(wl))

def count(filename, dbname):
    try:
        db = pytc.HDB(dbname, pytc.HDBOWRITER|pytc.HDBOCREAT)
        f = open(filename, "r")
        for line in f:
            [db.addint(w, 1) for w in split(line.rstrip("\n")) if w != ""]
                    
    except Exception, (errno, strerror):
        print strerror
    finally:
        db.close()

def word_and_count(input, output):
    i = open(input, "r")
    o = open(output, "w")
    
    for line in i:
        d = {}
        for w in split(line.rstrip("\n")):
            if w != "":
                if w in d:
                    d[w] += 1
                else:
                    d[w] = 1
        o.write(' '.join([str(k) + ' ' + str(n) for k, n in d.items()]))
        o.write("\n")
        o.flush()
        
def view(dbname):
    db = pytc.HDB(dbname, pytc.HDBOWRITER|pytc.HDBOCREAT)
    try:
        l = db.items()
        d = {}
        
        for item in l:
            d[item[0]] = db.addint(item[0], 0)
            
        for k, v in sorted(d.items(), key=lambda x:x[1]):
            print k, v
    except:
        pass
    finally:
        db.close()

if __name__ == '__main__':
    flatten("wikidump/all.txt", "wikidump/all.flatten.txt")
    count("wikidump/all.flatten.txt", "wikipedia.db")
    word_and_count("wikidump/all.flatten.txt", "wikidump/ldacorpus.txt")

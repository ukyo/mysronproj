#!/usr/bin/env python
#coding: utf8

import MeCab
import sys
import re
import os

HOME = os.environ["HOME"]
default_option = "-d %s/mecab-ipadic-2.7.0-20070801 -u %s/mecab-dic-overdrive/misc/dic/wikipedia.dic" % (HOME, HOME)
p = re.compile("[a-zA-Zぁ-んァ-ン]")
m = p.match
tagger = MeCab.Tagger(default_option)

def clean(input):
    i = open(input, "r")
    for line in i:
        line_ = line.strip("\n")
        lst = line_.split(" ")
        if int(lst[-1]) > 14:
            l = " ".join(lst[:-1])
        else:
            continue
        
        if len(l.decode("utf8")) == 1 and m(l) is not None:
            continue
        else:
            print l
    i.close()
    
if __name__ == '__main__':
    clean(sys.argv[1])
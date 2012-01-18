#!/usr/bin/env python
#coding: utf8

"""
PLDA用のコーパスを作る関数群です。
"""

import pytc
import sys
from hizukereader import Parser
import re

split = re.compile(",").split

def flatten(input, output):
    """
    wp2txtによって出力されたテキスト内の単語を
    カンマ区切りでい一行づつ出力する
    """
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
    """
    flattenで出力したテキストのから単語の頻度を数え上げる
    TokyoCabinetが必要です
    """
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
    """
    flattenで出力されたテキストから一行ごとに
    単語の種類と数の頻度を出力する
    Example:
    word1 1 word2 3 word3 2 .....
    word1 3 word3 1 word4 3 .....
    """
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

def word_and_count_ignore_stopword(input, output, wordfile):
    """word_and_countの改良版。wordfileにない単語は無視"""
    i = open(input, "r")
    o = open(output, "w")
    wf = open(wordfile, "r")
    
    wd = {}
    for l in wf:
        wd[l.rstrip("\n")] = 1
    for l in i:
        d = {}
        for w in split(l.rstrip("\n")):
            if w != "":
                if w in wd:
                    if w in d:
                        d[w] += 1
                    else:
                        d[w] = 1
        o.write(' '.join([str(k).replace(" ", "_") + ' ' + str(n) for k, n in d.items()]))
        o.write("\n")
        o.flush()
    
def view(dbname):
    """TokyoCabinetにためたデータから頻度を出力するだけの能力"""
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
    #flatten("wikidump/all2.txt", "wikidump/all.flatten2.txt")
    #count("wikidump/all.flatten2.txt", "wikipedia.db")
    #word_and_count("wikidump/all.flatten2.txt", "wikidump/ldacorpus2.txt")
    word_and_count_ignore_stopword("wikidump/allflatten.txt",
                                   "wikidump/ldacorpus3.txt",
                                   "hindocleaned.txt")

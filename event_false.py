#!/usr/bin/env python
#coding: utf8

import sys
import re
import datetime
import unicodedata
from NormalizeText import TextNormalizer

pattern_year = re.compile(u"([1-9][0-9]{3,})[\/年][0-9]")
normalizer = TextNormalizer()
tv_list = [
    u"nhk",
    u"テレ東", u"テレビ東京",
    u"日テレ", u"日本テレビ",
    u"テレビ朝日", u"テレ朝",
    u"tbs",
    u"フジテレビ"
]

def print_false_event(input):
    """
    イベントじゃないツイートを表示する
    """
    i = open(input, "r")
    for line in i:
        l = line.rstrip("\n")
        is_event = int(l.split("____")[1])
        if not is_event:
            print l

def print_true_event(input):
    """
    イベントであるツイートを表示する
    """
    i = open(input, "r")
    for line in i:
        l = line.rstrip("\n")
        is_event = int(l.split("____")[1])
        if is_event:
            print l



class Rule(object):
    """イベントではないツイートを見つけるためのルール"""
    rules = (
        "teiden", "tenki", "tuhan",
        "rekisi", "tv", "kojin_event",
        "end", "kojin_yotei"
    )
    
    def __init__(self, rules=[]):
        if len(rules) > 0:
            self.rules = rules[:]
        else:
            self.rulse = Rule.rules
    
    def is_event(self, s):
        "イベントかどうかの判断"
        if type(s).__name__ == "str":
            s = s.decode("utf8")
        s = normalizer.normalize(s)
        for rule in self.rules:
            if getattr(self, rule, lambda x: False)(s):
                return False
        return True
    
    def end(self, s):
        "終了している"
        return u"終了" in s
    
    def kojin_yotei(self, s):
        "個人的なイベント参加予定が列挙されてるだけのもの"
        return u"参加予定" in s or u"次回参加イベント" in s or u"イベ参加" in s
    
    def teiden(self, s):
        "停電関係"
        return u"停電" in s
    
    def tenki(self, s):
        "天気関係"
        return u"天気" in s or u"警報" in s or u"注意報" in s
    
    def tuhan(self, s):
        "通販関係"
        return u"受注生産" in s or u"通販" in s
    
    def rekisi(self, s):
        "過去の歴史関係"
        today = datetime.datetime.today()
        if u"何の日" in s:
            return True
        lst = pattern_year.findall(s)
        if len(lst) == 0:
            return False
        event_year = int(lst[0])
        return event_year < today.year
    
    def tv(self, s):
        "テレビ、録画予約など"
        if u"録画" in s or u"番組" in s:
            return True
        for channel in tv_list:
            if channel in s:
                return True
        return False
    
    def kojin_event(self, s):
        "個人的なイベント"
        return u"誕生日" in s or u"結婚式" in s or u"新年会" in s


def exec_rule(input):
    f = open(input)
    rule = Rule()
    for line in f:
        l = line.rstrip("\n")
        yield l + "===" + ("1" if rule.is_event(l) else "0")

def count(input):
    f = open(input)
    c = 0
    n = 0
    for line in f:
        l = line.rstrip("\n")
        lst1 = l.split("===")
        rule = lst1[1]
        human = lst1[0].split("____")[1]
        if rule == human:
            c += 1
        n += 1
    print "success: %d, n: %d" % (c, n)


if __name__ == '__main__':
    input = sys.argv[1]
    #exec_rule(input)
    count(input)
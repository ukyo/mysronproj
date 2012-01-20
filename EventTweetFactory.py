#!/usr/bin/env python
#coding: utf8

"""
通常のtweetにイベント情報を付加してくれる。
tweet:
  event_info:
    date
    place
    topic
    tokens
"""

import re
from NormalizeText import TextNormalizer
import datetime
from BeautifulSoup import BeautifulSoup as BS
from config import *
import urllib
import urllib2
import MeCabParser
import pldautils

pattern_year = re.compile(u"([1-9][0-9]{3,})[\/年][0-9]")
p_date = re.compile(u"[1-9]{1,2}[\/月][1-9]{1,2}[\/日]")
date_split = re.compile(u"[\/月日]").split
p_event = re.compile("^.*(本日|今日|明日|明後日|募集|予約|歓迎|発売|発表|開催|実施|参加|受付|会場|開場|申し込み|展示|開演|主催).*$")
p_youbi = re.compile(u"\([月火水木金土日]\)")
normalizer = TextNormalizer()
tv_list = [
    u"nhk",
    u"テレ東", u"テレビ東京",
    u"日テレ", u"日本テレビ",
    u"テレビ朝日", u"テレ朝",
    u"tbs",
    u"フジテレビ"
]
yurl="http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder"


def urlopen(q):
    if type(q).__name__ == "unicode":
        q = q.encode("utf8")
    return urllib2.urlopen(yurl+"?appid="+yid+"&query="+q)

class EventTweetTokenizer(MeCabParser.Parser):
    """tweetから余計なものを削除してトークナイズ"""
    
    def tokenize(self, s):
        """トークン化する"""
        s = p_date.sub('', s)
        s = p_youbi.sub('', s)
        tokens = self.parse(s)
        t = [n.surface for n in tokens]
        body = []
        for token in tokens:
            if not p_event.match(token.surface):
                body.append(token.surface)
            elif not "固有名詞,地域" in token.feature:
                body.append(token.surface)
        
        return tokens, body
    
    def delete_event_expr(self, s):
        """イベントに関係する表現を削除する"""
        
        s = p_event.sub('', s)
        
        return s
    
    def parse(self, s):
        """ちゃんとした名詞のみを抜き出す"""
        node = self.node(s)
        ret = []
        while node:
            surface = node.surface
            if surface != "" and "名詞" in node.feature and not "名詞,数" in node.feature and not "非自立" in node.feature:
                #if to_unicode:
                #    surface = surface.decode(self.encoding)
                ret.append(node)
            node = node.next
        return ret


class TweetTokenizer(MeCabParser.Parser):
    def parse(self, s):
        """ちゃんとした名詞のみを抜き出す"""
        node = self.node(s)
        ret = []
        while node:
            surface = node.surface
            if surface != "" and "名詞" in node.feature and not "名詞,数" in node.feature and not "非自立" in node.feature:
                #if to_unicode:
                #    surface = surface.decode(self.encoding)
                ret.append(surface)
            node = node.next
        return ret


class RuleBase(object):
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
            self.rulse = RuleBase.rules
    
    def is_event(self, s):
        """イベントかどうかの判断"""
        if type(s).__name__ == "str":
            s = s.decode("utf8")
        s = normalizer.normalize(s)
        for rule in self.rules:
            if getattr(self, rule, lambda x: False)(s):
                return False
        return True
    
    def end(self, s):
        """終了している"""
        return u"終了" in s
    
    def kojin_yotei(self, s):
        """個人的なイベント参加予定が列挙されてるだけのもの"""
        return u"参加予定" in s or u"次回参加イベント" in s or u"イベ参加" in s
    
    def teiden(self, s):
        """停電関係"""
        return u"停電" in s
    
    def tenki(self, s):
        """天気関係"""
        return u"天気" in s or u"警報" in s or u"注意報" in s
    
    def tuhan(self, s):
        """通販関係"""
        return u"受注生産" in s or u"通販" in s
    
    def rekisi(self, s):
        """過去の歴史関係"""
        today = datetime.datetime.today()
        if u"何の日" in s:
            return True
        lst = pattern_year.findall(s)
        if len(lst) == 0:
            return False
        event_year = int(lst[0])
        return event_year < today.year
    
    def tv(self, s):
        """テレビ、録画予約など"""
        if u"録画" in s or u"番組" in s:
            return True
        for channel in tv_list:
            if channel in s:
                return True
        return False
    
    def kojin_event(self, s):
        """個人的なイベント"""
        return u"誕生日" in s or u"結婚式" in s or u"新年会" in s


class EventTweetFactory(object):
    """イベントツイート作成用のクラス"""
    
    def __init__(self, wordlist):
        self.tokenizer = EventTweetTokenizer()
        self.rule_base = RuleBase()
        self.plda_formatter = pldautils.PLDAFormatter(wordlist)
    
    def get_event_tweets(self, tweets):
        """通常のtweetにイベント情報を付加"""
        if type(tweets) != list:
            tweets = [tweets]
        for tweet in tweets:
            if not self.rule_base.is_event(tweet['text']):
                continue
            tokens, body = self.tokenizer.tokenize(tweet['text'])
            words = map(lambda node: node.surface, tokens)
            bag_of_words = self.plda_formatter.format(body)
            if not "event_info" in tweet:
                tweet['event_info'] = {
                    "date": "",#self._date(tweet),
                    "place": self._place(tokens),
                    "body": body,
                    "tokens": map(lambda n: {"word":n.surface, "feature":n.feature}, tokens),
                    "topic": pldautils.get_topic_from_server_p(bag_of_words)
                }
            else:
                info = tweet["event_info"]
                info["body"] = body
                info["tokens"] = map(lambda n: {"word":n.surface, "feature":n.feature}, tokens)
                info["topic"] = pldautils.get_topic_from_server_p(bag_of_words)
            yield tweet
        
    def _place(self, tokens):
        """tweet内の場所情報を取得"""
        places = []
        for token in tokens:
            if "固有名詞,地域" in token.feature:
                places.append(token.surface)
        if len(places) > 0:
            u = urlopen(places[0])
            soup = BS(u.read())
            coord = soup.find("coordinates")
            if coord is not None:
                return map(float, coord.text.split(","))
        return None
    
    def _date(self, tweet):
        """tweet内の日付情報を取得"""
        lst = p_date.findall(tweet["text"])
        today = datetime.datetime.today()
        event_dates = []
        for d in lst:
            dd = date_split(d)
            event_dates.append({
                "y": today.year,
                "m": int(dd[0]),
                "d": int(dd[1])
            })
        return event_dates


if __name__ == "__main__":
    import config
    import json
    import sys
    fty = EventTweetFactory(config.wordfile)
    tokenizer = TweetTokenizer()
    f = open(sys.argv[1], "r")
    if sys.argv[2] == "1":
        recent = [json.loads(s) for s in f]
    elif sys.argv[2] == "2":
        recent = []
        [recent.extend(json.loads(t)) for t in f]
    elif sys.argv[2] == "3":
        formatter = pldautils.PLDAFormatter(config.wordfile)
        for s in f:
            status = json.loads(s)
            tokens = tokenizer.parse(status["text"])
            status["topic"] = pldautils.get_topic_from_server_p(formatter.format(tokens))
            print status
    else:
        pass
#        recent = json.load(f)
#    for tweet in fty.get_event_tweets(recent):
#        print json.dumps(tweet)
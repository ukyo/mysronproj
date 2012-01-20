#!/usr/bin/env python
#coding: utf8

import sys
from tinytwitter import tinytwitter as tw
import MeCabParser
import datetime
from config import *
import json
from pldautils import PLDAFormatter, get_topic_from_server
import MeCabParser


api = tw.Api(oauth)
backup = open("backup.txt", "w")

class Parser(MeCabParser.Parser):
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


class UserModelFactory(object):
    """
    ユーザモデルを生成するクラス
    prefixがloadｎのときはtwitterから読み込む
    getのときは基本的に内部だけで処理できる
    """
    
    def __init__(self, wordlist):
        self.formatter = PLDAFormatter(wordlist)
        self.parser = Parser()
    
    def get_user_model(self, user):
        """ユーザーモデルの生成"""
        self.log = open("log_"+user+".json", "w")
        lists = self.load_lists(user)
        tweets = []
        profiles = []
        for lst in lists:
            list_id = lst["id"]
            #tweets.extend(self.load_list_timeline(list_id))
            profiles.extend(self.load_member_profile(list_id))
        profiles_ = []
        for profile in profiles:
            profiles_.extend(self.parser.parse(profile))
        #tweets_ = [self.parser.parse(tweet) for tweet in tweets]
        #profiles_.extend(tweets)
        bag_of_words = self.formatter.format(profiles_)
        return {
            "bag_of_words": bag_of_words,
            "topic": self.get_topic(bag_of_words)
        }
    
    def get_topic(self, bag_of_words):
        return get_topic_from_server(bag_of_words)
    
    def load_lists(self, user):
        """twitterからlistを読み込む"""
        next_cursor = -1
        lists = []
        while next_cursor:
            try:
                r = api.lists__memberships(screen_name=user, cursor=next_cursor)
                lists.extend(r['lists'])
                next_cursor = r["next_cursor"]
            except:
                pass
        return lists
    
    def load_list_timeline(self, list_id):
        """listのタイムラインを読み込む"""
        tweets = []
        for i in range(1,3):
            try:
                r = api.lists__statuses(list_id=list_id,
                                        page=str(i),
                                        per_page=200)
                tweets.extend([tweet["text"] for tweet in r if len(tweet) > 30])
            except:
                pass
        return tweets
    
    def load_member_profile(self, list_id):
        """list内のすべてのユーザーのプロフィールを取得"""
        next_cursor = -1
        profiles = []
        i = 0
        while next_cursor and i < 3:
            try:
                r = api.lists__members(list_id=list_id, cursor=next_cursor)
                next_cursor = r["next_cursor"]
                #log
                self.log.write(json.dumps(r)+"\n")
                self.log.flush()
                profiles.extend([user["description"] for user in r["users"]])
            except:
                pass
            i += 1
        return profiles


if __name__ == '__main__':
    import config
    import sys
    user_model_factory = UserModelFactory(config.wordfile)
    user_model = user_model_factory.get_user_model(sys.argv[1])
    print json.dumps(user_model)
#coding: utf8


import math

class EventTweetRecommender(object):
    
    def __init__(self, event_tweet_models):
        self.tweet_models = event_tweet_models
        
    def calc(self, user_model, n=30, method="Dkl"):
        u_topic = user_model["topic"]
        t_topics = []
        for i, t_model in enumerate(self.tweet_models):
            kl = getattr(self, method)(u_topic, t_model["event_info"]["topic"])
            t_topics.append([i, kl])
        rank = sorted(t_topics, key=lambda x: x[1])
        ret = []
        i = 0
        while i < n:
            ret.append(self.tweet_models[rank[i][0]])
            i += 1
        return ret
        
    def Dkl(self, user, tweet):
        """KLダイバージェンス"""
        sum_ = 0
        for i in range(len(user)):
            sum_ += user[i] * (math.log(user[i] + 0.01) - math.log(tweet[i] + 0.01))
        return sum_ 
        
    def pro(self, user, tweet):
        sum_ = 0
        for i in range(len(user)):
            sum_ += user[i] * tweet[i]
        return sum_
    
if __name__ == '__main__':
    pass
Tiny Twitter API Wrapper
===

Example:
    import tinytwitter as tw
    
    consumer_key = 'your-consumer-key'
    consumer_secret = 'your-consumer-secret'
    token_key = 'access-token-key'
    token_secret = 'access-token-secret'
    
    auth = tw.OAuth(consumer_key, consumer_secret, token_key, token_secret)
    api = tw.Api(auth)
    
    #post a new tweet
    status = api.post(tw.STATUSES_UPDATE, status='message')
    
    #show home timeline
    for tweet in api.get(tw.STATUSES_HOME_TIMELINE):
        print tweet['text']
    
    #delete a tweet
    api.post(tw.STATUSES_DESTROY % status['id'])
    
    #create a new list
    list = api.post(tw.USER_LISTS % status['user']['screen_name'], name='foo')
    
    #delete a list
    api.delete(tw.USER_LISTS_ID % (status['user']['screen_name'], list['id']))
    
    def print_tweet(tweet):
        try:
            print tweet['text']
        except:
            pass
    
    #print sample stream
    api.get(tw.STREAM_SAMPLE, 'GET', print_tweet)

import tinytwitter as tw

user = raw_input('username:')
password = raw_input('password:')

api = tw.Api()

for line in api.statuses__public_timeline():
    print line['user']['screen_name']

auth = tw.BasicAuth(user, password)
api = tw.Api(auth)



for i, line in enumerate(api.filter_stream(track="twitter")):
    print line['user']['lang']
    if(i > 100):
        break
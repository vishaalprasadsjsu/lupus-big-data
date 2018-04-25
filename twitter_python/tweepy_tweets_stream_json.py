import tweepy 
from tweepy import OAuthHandler 
from tweepy import Stream
from tweepy.streaming import StreamListener

import keys
 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

# prepare api/tweepy
auth = OAuthHandler(keys.app_key, keys.app_secret)
auth.set_access_token(keys.oauth_token, keys.oauth_token_secret)

api = tweepy.API(auth)

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])
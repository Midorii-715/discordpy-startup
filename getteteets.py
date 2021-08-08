import tweepy
import re

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
   def on_status(self, status):
       if "@" in status.text:
           pass
       else:
           print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(follow=["qu_youmu"], is_async=True)

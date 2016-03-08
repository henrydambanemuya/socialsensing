from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy

#from auth import TwitterAuth

#Very simple (non-production) Twitter stream example
#1. Download / install python and tweepy (pip install tweepy)
#2. Fill in information in auth.py
#3. Run as: python streaming_simple.py
#4. It will keep running until the user presses ctrl+c to exit
#All output stored to output.json (one tweet  per line)
#Text of tweets also printed as recieved (see note about not doing this in production (final) code

# Consumer keys and access tokens, used for OAuth
consumer_key = 'bk4l0l0rHdiZMJWZW9pNZQVUq'
consumer_secret = 'EK1kYIqFTBYsrFGWqTUB0OEKg9ZZk7igc3CYiaMTzK19V8qJPS'
access_token = '219557776-l5XshDUG0VKq0uJm9R83oHYr2v7PHnkem1IK9wFl'
access_secret = 'DH0USra44ykbGlfj3DaS8FWTjRWuatKxiSI9Te0Ni1amM'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('data.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
stream = Stream(auth, MyListener())
stream.filter(track=['Donald Trump'])

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy
import re

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
access_token_secret = 'DH0USra44ykbGlfj3DaS8FWTjRWuatKxiSI9Te0Ni1amM'


class StdOutListener(StreamListener):

  #This function gets called every time a new tweet is received on the stream
  def on_data(self, data):
    #Just write data to one line in the file
    fhOut.write(data)

    #Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
    j=json.loads(data)

    #See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
    text=j["text"] #The text of the tweet
    user=j["user"] #The user data
    screen_name=user["screen_name"] #The user screen name
    location=user["location"]
    timestamp=j["created_at"]
    streamText=open('streamText.txt', 'a', encoding='utf-8')
    streamText.write(str(text) + " Screen_Name:@" + str(screen_name) + " Location:" + str(location) + " Timestamp:" + str(timestamp) + "\n"*2)

  def on_error(self, status):
    print("ERROR")
    print(status)

if __name__ == '__main__':
  try:
    #Create a file to store output. "a" means append (add on to previous file)
    fhOut = open("output.json","a", encoding='utf-8')

    #Create the listener
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #Connect to the Twitter stream
    stream = Stream(auth, l)

    #Terms to track
    stream.filter(track=["peacetech","scalepeacetech"])

    #Alternatively, location box  for geotagged tweets?,
    #stream.filter(locations=[-0.530, 51.322, 0.231, 51.707])

  except KeyboardInterrupt:
    #User pressed ctrl+c -- get ready to exit the program
    pass

  #Close the
  fhOut.close()

#Tweet Search
#Author: Henry K. Dambanemuya, University of Notre Dame

import tweepy
 
# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Create a list of user profile ID's
userList = [34373370, 26257166, 12579252]
 
# Task 1: Collecting user's profile information 
def task1():
    # Create text document to store twitter profiles
    userProfilesFile = open('userProfiles.txt', 'w', encoding='utf-8')
    # Download user profiles information and print each profile to text file
    for userId in userList:
        user = api.get_user(userId)
        userProfilesFile.write ("Screen Name: " + str(user.screen_name) + "\n")
        userProfilesFile.write ("User Name: " + str(user.name) + "\n")
        userProfilesFile.write ("User Location: " + str(user.location) + "\n")
        userProfilesFile.write ("User Description: " + str(user.description) + "\n")
        userProfilesFile.write ("The Number of Followers: " + str(user.followers_count) + "\n")
        userProfilesFile.write ("The Number of Friends: " + str(user.friends_count) + "\n")
        userProfilesFile.write ("The Number of Statuses: " + str(user.statuses_count) + "\n")
        userProfilesFile.write ("User URL: " + str(user.url) + "\n"*2)
    userProfilesFile.close()

# Task 2: Collecting user's social network information 
def task2():
    # Create text document and download lists of screen names of the user's friends and followers lists and print results to text file
    friendListFile = open('friendList.txt', 'w', encoding='utf-8')
    for userId in userList:
        user = api.get_user(userId)
        # Download lists of screen names of the user's friends and print results to text file
        friendListFile.write (str(user.name) + " Friends List:" + "\n"*2)
        for friend in user.friends():
            friendListFile.write (str(friend.screen_name) + "\n")
        friendListFile.write ("\n")
        # Download lists of screen names of the user's followers and print results to text file
        friendListFile.write (str(user.name) + " Followers List:" + "\n"*2)
        for follower in user.followers():
            friendListFile.write (str(follower.screen_name) + "\n")
        friendListFile.write ("\n")
    friendListFile.close()

# Task 3a: Collecting tweets that contain one of the following two keywords: [Indiana, weather] 
def task3a():
    # Create text document and download tweets that contain one of the following two keywords: [Indiana, weather] and print results to text file
    keywordSearchFile = open('keywordSearch.txt', 'w', encoding='utf-8')
    for tweet in tweepy.Cursor(api.search,q="Indiana OR weather", lang="en").items(50):
        keywordSearchFile.write (str(tweet.text) + "\n")
    keywordSearchFile.close()

# Task 3b: Collecting tweets that originate from the geographic region around South Bend: [-86.33,41.63,-86.20,41.74].
def task3b():
    #Convert Longitude of left point, Latitude of left point, Longitude of right point, Latitude of right point to [Latitude, longitude, radius]
    radius = "10km"
    latitude = ((41.74+41.63)/2)
    longitude = (((-86.33)+(-86.20))/2)
    coordinates = str(latitude) + "," + str(longitude) + "," + str(radius)
    # Create text document and download tweets that originate from the geographic region around South Bend: [-86.33,41.63,-86.20,41.74]
    geocodeSearchFile = open('geocodeSearch.txt', 'w', encoding='utf-8')
    for tweet in tweepy.Cursor(api.search,q="*", lang="en", geocode=coordinates).items(50):
        geocodeSearchFile.write (str(tweet.text) + "\n")
    geocodeSearchFile.close()

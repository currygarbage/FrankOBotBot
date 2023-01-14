# Import needed dependencies
import tweepy
import time
import requests
from lyricsgenius import Genius
from info import credentials, info
from src.reply import reply
from src.getImage import getImage

# Log into both Tweepy 2.0 and 1.0
client = tweepy.Client(
    credentials['BEARER_TOKEN'],
    credentials['API_KEY'],
    credentials['API_SECRET'],
    credentials['ACCESS_TOKEN'],
    credentials['ACCESS_SECRET']
)

auth = tweepy.OAuth1UserHandler(
    credentials['API_KEY'],
    credentials['API_SECRET'],
    credentials['ACCESS_TOKEN'],
    credentials['ACCESS_SECRET']
)
api = tweepy.API(auth)

# Log into Genius
genius = Genius(credentials['GENIUS_TOKEN'])

# Get latest tweet for account to reply
prevTweets = api.user_timeline(screen_name=info['account'], count=1)

# Set up no-album
noAlbum = info['noAlbum']

# Listen for new tweets in comparison to prev. tweets
while True:
    newTweets = api.user_timeline(screen_name=info['account'], count=1)
    if newTweets == prevTweets:
        print('No new tweets')
    else:
        print('Account tweeted')
        getImage(newTweets, genius, requests)
        reply(newTweets, api, client, genius, noAlbum)
    prevTweets = newTweets
    
    # 30 sec. cool down to avoid overproccessing
    time.sleep(30)
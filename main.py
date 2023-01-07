# Import needed dependencies
import tweepy
import time
import os
import requests
from lyricsgenius import Genius
from info import credentials, info

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

def getImage(tweets):
    for tweet in tweets:
        lyric = tweet.text.strip()

    # Search for song to get album cover
    url = genius.search_songs(lyric)['hits'][0]['result']['song_art_image_url']

    # Turn link into image
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

def reply(tweets):
    for tweet in tweets:
        lyric = tweet.text.strip()
        tweetId = tweet.id

    # Main lines of code that searches for the lyric
    song = genius.search_lyrics(lyric)
    id = song['sections'][0]['hits'][0]['result']['id']
    songData = genius.song(id)

    songName = song['sections'][0]['hits'][0]['result']['title']

    # Get song name, album name
    if songData['song']['album'] == None:
        albumName = songName
    else:
        albumName = songData['song']['album']['name'].strip()

    for i in range(len(noAlbum)):
        if noAlbum[i] in albumName:
            albumName = songName

    if albumName.endswith('.'):
        reply = f'"{songName}" from album {albumName}'
    else:
        reply = f'"{songName}" from album {albumName}.'

    # Update profile image and reply to account
    api.update_profile_image('temp.jpg')
    client.create_tweet(text=reply, in_reply_to_tweet_id=tweetId)

    # Remove profile image from repository
    os.remove('temp.jpg')

# Listen for new tweets in comparison to prev. tweets
while True:
    newTweets = api.user_timeline(screen_name='frankolyricsbot', count=1)
    if newTweets == prevTweets:
        print('No new tweets')
    else:
        print('Account tweeted')
        getImage(newTweets)
        reply(newTweets)
    prevTweets = newTweets
    
    # 30 sec. cool down to avoid overproccessing
    time.sleep(30)
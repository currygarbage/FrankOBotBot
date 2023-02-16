# Import needed dependencies
import tweepy
import os
from lyricsgenius import Genius
from info import credentials, info
from getImage import getImage

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

# Set up no-album list
noAlbum = info['noAlbum']

# Get tweets from target account
tweets = api.user_timeline(screen_name=info['target'], count=1)
myTweets = api.user_timeline(screen_name=info['account'], count=1)

# Get tweet content
for tweet in tweets:
    lyric = tweet.text.strip()
    tweetId = tweet.id

for tweet in myTweets:
    inReplyTo = tweet.in_reply_to_status_id

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

url = song['hits'][0]['result']['song_art_image_url']

# Print + tweet reply
print(reply)
if (inReplyTo == tweetId):
    print('I already replied!')
else:
    client.create_tweet(text=reply, in_reply_to_tweet_id=tweetId)

    # Get album cover file
    getImage(url)

    #Update profile image
    api.update_profile_image('temp.jpg')
    os.remove('temp.jpg')
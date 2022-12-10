import tweepy
import datetime
from lyricsgenius import Genius
from secret import credentials, log

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

genius = Genius(credentials['GENIUS_TOKEN'])

lyrics = api.user_timeline(user_id=1264110032875999234, count=1)
    
for tweet in lyrics:
    lyric = tweet.text.strip()
    tweetID = tweet.id

song = genius.search_lyrics(lyric)
id = song['sections'][0]['hits'][0]['result']['id']
songData = genius.song(id)

songName = song['sections'][0]['hits'][0]['result']['title']
if(songData['song']['album'] == None):
    albumName = songName
else:
    albumName = songData['song']['album']['name'].strip()

if(albumName == 'FO3*'):
    albumName = songName

if(albumName.endswith('.')):
    reply = f'"{songName}" from album {albumName}'
else:
    reply = f'"{songName}" from album {albumName}.'

client.create_tweet(text=reply, in_reply_to_tweet_id=tweetID)
log(datetime.datetime.now())

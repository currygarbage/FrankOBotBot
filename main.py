import tweepy
import time
import os
import requests
from lyricsgenius import Genius
from server import keep_alive

client = tweepy.Client(
    os.environ['BEARER_TOKEN'],
    os.environ['API_KEY'],
    os.environ['API_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_SECRET']
)

auth = tweepy.OAuth1UserHandler(
    os.environ['API_KEY'],
    os.environ['API_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_SECRET']
)
api = tweepy.API(auth)

genius = Genius(os.environ['GENIUS_TOKEN'])

prevTweets = api.user_timeline(screen_name='frankolyricsbot', count=1)

noAlbum = ['FO3*', 'Blonded Los Santos 97.8 FM [GTA V]', '7" Vinyl Single']

def reply(tweets):
    for tweet in tweets:
        lyric = tweet.text.strip()
        tweetId = tweet.id

    song = genius.search_lyrics(lyric)
    id = song['sections'][0]['hits'][0]['result']['id']
    songData = genius.song(id)

    songName = song['sections'][0]['hits'][0]['result']['title']
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

    api.update_profile_image('temp.jpg')
    client.create_tweet(text=reply, in_reply_to_tweet_id=tweetId)
    os.remove('temp.jpg')

def getImage(tweets):
    for tweet in tweets:
        lyric = tweet.text.strip()

    url = genius.search_songs(lyric)['hits'][0]['result']['song_art_image_url']
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

keep_alive()

while True:
    newTweets = api.user_timeline(screen_name='frankolyricsbot', count=1)
    if newTweets == prevTweets:
        print('No new tweets')
    else:
        print('Account tweeted')
        getImage(newTweets)
        reply(newTweets)
    prevTweets = newTweets
    time.sleep(30)
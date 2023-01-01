import tweepy
import lyricsgenius
import os
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

genius = lyricsgenius.API(os.environ['GENIUS_TOKEN']) 

noAlbum = ['FO3*', 'Blonded Los Santos 97.8 FM [GTA V]', '7" Vinyl Single']

class listener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        lyric = tweet.text.strip()
        tweetID = tweet.id

        song = genius.search_songs(lyric)['hits'][0]['result']
        id = song['id']
        songData = genius.song(id)

        songName = genius.search_songs(lyric)['hits'][0]['result']['title']

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

        client.create_tweet(text=reply, in_reply_to_tweet_id=tweetID)
        print(reply)

    def on_error(self, status_code):
      if status_code == 420:
        print('Rate limit')
        return False
  
keep_alive()

stream = listener(os.environ['BEARER_TOKEN'])
stream.add_rules(tweepy.StreamRule('from:frankolyricsbot'))
print(stream.get_rules())
stream.filter()
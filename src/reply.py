# Import needed dependencies
import os
from info import credentials, info

def reply(tweets, tweepyAPI, tweepyClient, geniusClient, noAlbum):
    # Set up clients
    api = tweepyAPI
    client = tweepyClient
    genius = geniusClient

    # Get tweet content
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
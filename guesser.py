from lyricsgenius import Genius
from info import credentials, info

def guessSong(lyrics):
    # Set up Genius + no-album
    genius = Genius(credentials['GENIUS_TOKEN'])
    noAlbum = info['noAlbum']

    # Main lines of code that searches for the lyric
    song = genius.search_songs(lyrics)
    id = song['hits'][0]['result']['id']
    songData = genius.song(id)
    
    songName = song['hits'][0]['result']['title']
    
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

    return reply
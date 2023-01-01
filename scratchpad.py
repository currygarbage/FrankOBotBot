# This is a file to test lyrics in the console

import lyricsgenius
import os

genius = lyricsgenius.API(os.environ['GENIUS_TOKEN'])

noAlbum = ['FO3*', 'Blonded Los Santos 97.8 FM [GTA V]', '7" Vinyl Single']

lyric = 'TEST LYRIC HERE'

song = genius.search_songs(lyric)['hits'][0]['result']
id = song['id']
songData = genius.song(id)

songName = genius.search_songs(lyric)['hits'][0]['result']['title']

if(songData['song']['album'] == None):
    albumName = songName
else:
    albumName = songData['song']['album']['name'].strip()

for i in range(len(noAlbum)):
    if noAlbum[i] in albumName:
        albumName = songName

if(albumName.endswith('.')):
    reply = f'"{songName}" from album {albumName}'
else:
    reply = f'"{songName}" from album {albumName}.'

print(reply)
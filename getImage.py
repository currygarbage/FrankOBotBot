def getImage(tweets, geniusClient, requests):
    # Set up clients
    genius = geniusClient

    # Get tweet content
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
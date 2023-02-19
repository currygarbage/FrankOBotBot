# FrankOBotBot
Replies to [@FrankOLyricsBot](https://twitter.com/FrankOLyricsBot) with the song name

## Usage
This program comes with a GPL-3.0 license. Use this program however you'd like with no warranty.

### Dependencies
- [tweepy](https://pypi.org/project/tweepy/)
- [lyricsgenius](https://pypi.org/project/lyricsgenius/)
- [A Twitter Developer account](https://developer.twitter.com)
- [A Genius Developer app](https://genius.com/api-clients)

### Guide 
1. Clone this repository
2. Add all the necessary information in the info.example.py file 
3. Rename it to info.py
4. Install all needed dependencies
5. Run reply.py locally or every hour (cronjob)

### Result
In the console, it should return the song and album name of the target account's latest tweet. The bot will also reply and change its profile image to the album cover, if it hasn't already.

For any issues, please submit a GitHub issue and I will help you out.

### Note
Occasionaly, it will reply with an incorrect song title if the lyric is a close match. This is a result of Genius's end, apologies for the confusion.

### Thanks
Thanks to [@mitskibotbot](https://twitter.com/mitskibotbot) for this Twitter bot idea.
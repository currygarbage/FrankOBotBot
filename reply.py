# Import needed dependencies
import tweepy
import guesser
from info import credentials, info

def main():
    # Client for replying
    client = tweepy.Client(
        credentials['BEARER_TOKEN'],
        credentials['API_KEY'],
        credentials['API_SECRET'],
        credentials['ACCESS_TOKEN'],
        credentials['ACCESS_SECRET']
    )
    
    # Client for getting tweets
    auth = tweepy.OAuth1UserHandler(
        credentials['API_KEY'],
        credentials['API_SECRET'],
        credentials['ACCESS_TOKEN'],
        credentials['ACCESS_SECRET']
    )
    api = tweepy.API(auth)
    
    # Get tweets from target account
    tweets = api.user_timeline(screen_name=info['target'], count=1)
    myTweets = api.user_timeline(screen_name=info['account'], count=1)
    
    # Get tweet content
    for tweet in tweets:
        lyric = tweet.text.strip()
        tweetId = tweet.id
    
    for tweet in myTweets:
        inReplyTo = tweet.in_reply_to_status_id
    
    # Guess song from tweet
    reply = guesser.guessSong(lyric)

    # Print + tweet reply
    print(reply)
    
    if (inReplyTo == tweetId):
        print('I already replied!')
    else:
        api.update_status(status=reply, in_reply_to_status_id=tweetId)

if __name__ == '__main__':
    main()
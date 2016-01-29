from main.twitterlib.tweet import Tweet
from twython import TwythonError
from main.twitterlib import connection

def collect_tweets_for_user(user,passwordfolder,exclude_retweets=False):

    twitter_connection = connection.create_twitter_connection(passwordfolder)
    no_tweets_received = False
    all_tweets = []
    page = 1

    while not no_tweets_received:

        try:
            new_raw_tweets = twitter_connection.get_user_timeline(screen_name=user,count=200,page=page)
        except TwythonError:
            new_raw_tweets = []
            print('Twython is sad :(')
            break

        if len(new_raw_tweets) < 1:
            no_tweets_received = True
        else:

            for raw_tweet in new_raw_tweets:
                current_tweet = Tweet(raw_tweet['id'],raw_tweet['user']['screen_name'],clean_tweet_text(raw_tweet['text']))
                if (exclude_retweets and current_tweet.content[2:5] != 'RT ') or not exclude_retweets:             
                    all_tweets.append(current_tweet)

        page += 1

    return all_tweets
    
def clean_tweet_text(tweet_text):

    tweet_text = tweet_text.encode('utf8')
    result = str(tweet_text).replace('\n','')

    return result

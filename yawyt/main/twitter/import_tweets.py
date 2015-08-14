import os
import random
from tweet import Tweet
from twython import Twython, TwythonError

def get_passwords_from_a_random_password_file(passwordfolder):

    passwordfilename = random.choice(os.listdir(passwordfolder))
    lines = open(passwordfilename,'r').readlines()
    passwords = {}

    for n,i in enumerate(lines):
        if i[0] == '#':
            passwords[i[1:].strip()] = lines[n+1].strip()

    return passwords

def collect_tweets_for_user(user,passwordfolder):

    passwords = get_passwords_from_a_random_password_file(passwordfolder)
    twitter_connection = Twython(passwords['app_key'], passwords['app_secret'],
              passwords['oauth_token'], passwords['oauth_token_secret'])

    no_tweets_received = False
    all_tweets = []
    page = 1

    while not no_tweets_received:

        try:
            new_raw_tweets = twitter_connection.get_user_timeline(screen_name=user,count=200,page=c)
        except TwythonError:
            new_raw_tweets = []
            print('Twython is sad :(')
            break

        if len(new_raw_tweets) < 1:
            no_tweets_received = True
        else:

            for raw_tweet in new_raw_tweets:
                current_tweet = Tweet(raw_tweet['id'],'wessel',clean_tweet_text(raw_tweet['text']))
                all_tweets.append(current_tweet)

        page += 1

    return all_tweets
    
def clean_tweet_text(tweet_text):

    tweet_text = tweet_text.encode('utf8')
    result = str(tweet_text).replace('\n','')

    return result
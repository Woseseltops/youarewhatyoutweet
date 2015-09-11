import os
import random
from twython import Twython

def get_passwords_from_a_random_password_file(passwordfolder):

    passwordfilename = random.choice(os.listdir(passwordfolder))
    lines = open(passwordfolder+passwordfilename,'r').readlines()
    passwords = {}

    for n,i in enumerate(lines):
        if i[0] == '#':
            passwords[i[1:].strip()] = lines[n+1].strip()

    return passwords

def create_twitter_connection(passwordfolder):

    passwords = get_passwords_from_a_random_password_file(passwordfolder)
    return Twython(passwords['app_key'], passwords['app_secret'],
              passwords['oauth_token'], passwords['oauth_token_secret'])

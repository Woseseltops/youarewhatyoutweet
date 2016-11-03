from sys import argv
from urllib.request import urlopen
from multiprocessing import Pool
from time import sleep

from os import mkdir
from shutil import rmtree

def visit_analyze_page(user):

    URL = 'http://applejack.science.ru.nl/youarewhatyoutweet/analyze/'
    r = urlopen(URL+user).read()
    print('Did request for',user)
    # sleep(60) #Estimate average time the user wil spend at the analyze page
    return r

def scrape_twitter_users(input_file_path):

    twitter_users = []

    for line in open(input_file_path):
        for word in line.split():
            if word[0] == '@':
                twitter_users.append(word[1:])

    return twitter_users

def start_stress_test(twitter_names,number_of_cores):

    pool = Pool(number_of_cores)
    result = pool.map(visit_analyze_page,twitter_names)

if __name__ == '__main__':

    DELETE_CACHE = True
    CACHE_ROOT = '/home/wessel/yawyt/yawyt/main/data/'

    FILE_PATH = '100_invloedrijkste_twitteraars.txt'
    twitter_users = scrape_twitter_users(FILE_PATH)

    try:

        if DELETE_CACHE:
            for folder_path in ['classifications','logs','tweets']:
                rmtree(CACHE_ROOT+folder_path)
                mkdir(CACHE_ROOT+folder_path)

        number_of_twitter_users = int(argv[1])
        number_of_cores = int(argv[2])

        start_stress_test(twitter_users[0:number_of_twitter_users],number_of_cores)
    except IndexError:
        print('python3 stress_test.py [number_of_accounts] [number_of_cores]')
        print('The number of accounts indicates the amount of work, the number of cores how much is fired at YAWYT at the same time.')
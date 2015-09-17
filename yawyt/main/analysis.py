from main.twitterlib.tweet import tweet_list_to_files_per_author, tweet_annotations_to_files_per_author
from main.twitterlib.import_tweets import collect_tweets_for_user
from main.models import ClassifierSection
import yawyt.settings as settings
import importlib
from threading import Thread

def start_analysis_thread_for_user(user):

    #Remove the @ if the user put it in
    if user[:3] == '%40':
        user = user[3:]

    Thread(target=analyze_tweets_of_user,args=([user])).start()

def analyze_tweets_of_user(user):
    refresh_logfile_for_user(user)
    log_progress_for_user('Collecting tweets for '+user, user)
    tweets = collect_tweets_for_user(user,settings.PASSWORD_FOLDER)
    tweet_list_to_files_per_author(tweets, settings.TWEET_DATAFOLDER)
    log_progress_for_user('Collecting tweets completed', user)

    log_progress_for_user('Analyzing tweets for user '+user, user)

    for classifier_section in ClassifierSection.objects.all():
        classifier_module = importlib.import_module('main.classifiers.'+classifier_section.classifier_module_name)
        classifier_class = getattr(classifier_module,classifier_section.classifier_class_name)
        classifier = classifier_class()

        for tweet in tweets:
            classifier.classify(tweet)

    tweet_annotations_to_files_per_author(tweets,settings.CLASSIFICATION_DATAFOLDER)

    log_progress_for_user('Finished analysis', user)


def refresh_logfile_for_user(user):
    open(settings.ANALYSIS_LOGFOLDER+user+'.txt','w')

def log_progress_for_user(message,user):

    print(message)
    open(settings.ANALYSIS_LOGFOLDER+user+'.txt','a+').write(message+'\n')

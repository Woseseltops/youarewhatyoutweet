from main.twitterlib.tweet import tweet_list_to_files_per_author, tweet_annotations_to_files_per_author
from main.twitterlib.import_tweets import collect_tweets_for_user
from main.classifiers import gender_classifier, age_classifier, aggression_classifier, predictability_classifier, sarcasm_classifier
from main.models import ClassifierSection
import yawyt.settings as settings
import importlib
import os
import time

from threading import Thread
from multiprocessing import Process, Queue, Pool

def start_analysis_thread_for_user(user):

    #Remove the @ if the user put it in
    if user[:3] == '%40':
        user = user[3:]

    #Skip if recent data are already found
    if settings.CACHING:
        first_classifier_name = ClassifierSection.objects.all()[0].classifier_module_name
        first_classifier_output_path = settings.CLASSIFICATION_DATAFOLDER + user + '.' + first_classifier_name + '.txt'

        if os.path.isfile(first_classifier_output_path) and \
            time.time() - os.path.getmtime(first_classifier_output_path) < settings.CACHING_RECENCY_BOUNDARY:
            return

    Thread(target=analyze_tweets_of_user,args=([user])).start()

def classify_tweets_with_classifier(classifier,tweets,finished_classifiers_queue):

    #First train if necessary
    if not classifier.fixed_model:
        classifier.train(tweets)

    #Don't process all tweets in parallel
    pool = Pool(settings.NUMBER_OF_PARALLEL_CLASSIFICATION_PROCESSES)
    tweets = pool.map(classifier.classify, tweets)

    #we're done, save the results and tell the rest we're done
    classifier.complete()
    tweet_annotations_to_files_per_author(tweets,settings.CLASSIFICATION_DATAFOLDER)
    finished_classifiers_queue.put(classifier)

def analyze_tweets_of_user(user):
    refresh_logfile_for_user(user)
    log_progress_for_user('Collecting tweets for '+user, user)
    tweets = collect_tweets_for_user(user,settings.PASSWORD_FOLDER,exclude_retweets=True)
    tweet_list_to_files_per_author(tweets, settings.TWEET_DATAFOLDER)
    log_progress_for_user('Collecting tweets completed', user)
                  
    log_progress_for_user('Analyzing tweets for user '+user, user)

    finished_classifiers = Queue()
    nr_of_classifiers = len(ClassifierSection.objects.all())

    for classifier_section in ClassifierSection.objects.all().order_by('position'):
        classifier_module = importlib.import_module('main.classifiers.'+classifier_section.classifier_module_name)
        classifier_class = getattr(classifier_module,classifier_section.classifier_class_name)
        classifier = classifier_class()

        if classifier_section.number_of_tweets_to_analyze == 0:
            tweets_to_analyze = tweets
        else:
            tweets_to_analyze = tweets[:classifier_section.number_of_tweets_to_analyze]

        Process(target=classify_tweets_with_classifier,args=[classifier,tweets_to_analyze,finished_classifiers]).start()

    #Here, we check the number of finished classifier one by one, to prevent them writing to the log file at the same time
    nr_of_finished_classifiers = 0

    while True:

        if nr_of_finished_classifiers < finished_classifiers.qsize():
            nr_of_finished_classifiers = finished_classifiers.qsize()
            log_progress_for_user('Finished analysis '+str(nr_of_finished_classifiers)+'/'+str(nr_of_classifiers), user)

            if nr_of_finished_classifiers == nr_of_classifiers:
                break

def refresh_logfile_for_user(user):
    open(settings.ANALYSIS_LOGFOLDER+user+'.txt','w')

def log_progress_for_user(message,user):

    print(message)
    open(settings.ANALYSIS_LOGFOLDER+user+'.txt','a+').write(message+'\n')

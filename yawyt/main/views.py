from django.shortcuts import render
from django.http import HttpResponse
from models import ClassifierSection
from twitter.tweet import tweet_list_to_files_per_author, tweet_annotations_to_files_per_author
from twitter.import_tweets import collect_tweets_for_user
import yawyt.yawyt.settings as settings

# Create your views here.

def twittername_entry(request):
    return render(request,'twittername_entry.html')

def analyze(request,user):

    log_progress_for_user('Collecting tweets for '+user)
    tweets = collect_tweets_for_user(user)
    tweet_list_to_files_per_author(tweets,settings.TWEET_DATAFOLDER)
    log_progress_for_user('Collecting tweets completed')

    log_progress_for_user('Analyzing tweets for user '+user)

    for classifier_section in ClassifierSection.objects.all():
        classifier = __import__('classifiers.'+classifier_section.classifier_module_name,fromlist=[classifier_section.classifier_class_name])

        for tweet in tweets:
            classifier.classify(tweet)

    tweet_annotations_to_files_per_author(tweets,settings.CLASSIFICATION_DATAFOLDER)

    log_progress_for_user('Finished analysis')

    return render(request,'analyze.html')

def log(request,user):

    return HttpResponse(open(settings.ANALYSIS_LOGFOLDER+user+'.txt').read())

def results(request):

    return render(request,'result_overview.html',{'classifier_sections':ClassifierSection.objects.all()})

def log_progress_for_user(message,user):

    print(message)
    open(settings.ANALYSIS_LOGFOLDER+user+'.txt','a').write(message+'\n')
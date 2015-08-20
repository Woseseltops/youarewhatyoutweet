from django.shortcuts import render
from django.http import HttpResponse
from models import ClassifierSection
import yawyt.settings as settings
from twitter.tweet import file_to_tweet_dict
from analysis import start_analysis_thread_for_user

# Create your views here.


def twittername_entry(request):
    return render(request,'twittername_entry.html')


def analyze(request,user):

    start_analysis_thread_for_user(user)
    return render(request,'analyze.html',{"user":user})


def log(request, user):

    return HttpResponse(open(settings.ANALYSIS_LOGFOLDER+user+'.txt').read())


def results(request,user):

    all_tweets_for_user = file_to_tweet_dict(settings.TWEET_DATAFOLDER+user+'.txt')

    #Add the annotations for all classifiers
    most_extreme_tweets = {}

    for classifier_section in ClassifierSection.objects.all():

        most_extreme_tweets[classifier_section.classifier_module_name] = all_tweets_for_user.values()[:5]
        print(most_extreme_tweets)

    return render(request,'result_overview.html',{'classifier_sections':ClassifierSection.objects.all(),
                                                  'most_extreme_tweets':most_extreme_tweets})
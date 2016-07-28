from django.shortcuts import render
from django.http import HttpResponse, Http404
from main.models import ClassifierSection
import yawyt.settings as settings
from main.twitterlib.tweet import file_to_tweet_dict, add_annotations_in_files_to_tweets
from main.twitterlib.profile_image import get_profile_image_url
from main.analysis import start_analysis_thread_for_user

import os

# Create your views here.


def twittername_entry(request):
    return render(request,'twittername_entry.html')


def analyze(request,user):

    start_analysis_thread_for_user(user)
    return render(request,'analyze.html',{"user":user})


def log(request, user):

    return HttpResponse(open(settings.ANALYSIS_LOGFOLDER+user+'.txt').read())


def calculate_meterscore_for_class_based_on_tweets(classifier_name,classname,tweets):

    scores = [tweet.automatic_classifications[classifier_name][classname] for tweet in tweets]
    return int(100*(sum(scores) / len(scores)))

def figure_out_username_capitalization(user):

    for filename in os.listdir(settings.TWEET_DATAFOLDER):

        filename_without_extension = filename.replace('.txt','')

        if filename_without_extension.lower() == user.lower():
            return filename_without_extension

def individual_classifier_result(request,user,classifier_name):

    #Find the classifier object
    classifier = None

    for classifier_section in ClassifierSection.objects.all():

        if classifier_section.classifier_module_name == classifier_name+'_classifier':
            classifier = classifier_section
            break

    if classifier == None:
        raise Http404("No classifier with this name is defined")

    all_tweets_for_user = file_to_tweet_dict(settings.TWEET_DATAFOLDER+user+'.txt')

    try:
        add_annotations_in_files_to_tweets(settings.CLASSIFICATION_DATAFOLDER + user + '.' + classifier_name + '_classifier.txt',
                                   classifier_name, all_tweets_for_user)
    except FileNotFoundError:
        return HttpResponse(-1);

    # Prepare saving the most extreme scores for each class for this classifier
    most_extreme_tweets = {}
    meterscores_per_class = {}

    # See what classes there are for this classifier, by taking them from a random tweet
    classes_for_this_classifier = list(
        all_tweets_for_user[list(all_tweets_for_user.keys())[0]].automatic_classifications[classifier_name].keys())

    # For each class, take the most extreme cases
    for classname in classes_for_this_classifier:
        all_tweets_sorted_by_confidence_for_this_class = sorted(all_tweets_for_user.values(), key=lambda tweet:
        tweet.automatic_classifications[classifier_name][classname], reverse=True)
        most_extreme_tweets[classname] = all_tweets_sorted_by_confidence_for_this_class[
                                                          :settings.NUMBER_OF_TWEETS_TO_SHOW_PER_CLASS]

        if classifier_section.number_of_tweets_in_score_calculation == 0:
            tweets_to_use_for_meter_score = all_tweets_sorted_by_confidence_for_this_class
        else:
            tweets_to_use_for_meter_score = all_tweets_sorted_by_confidence_for_this_class[
                                            :classifier_section.number_of_tweets_in_score_calculation]

        meterscores_per_class[classname] = calculate_meterscore_for_class_based_on_tweets(classifier_name,classname,tweets_to_use_for_meter_score)

    return render(request, classifier_name+'_content.html',
                  {
                   'most_extreme_tweets': most_extreme_tweets,
                   'meterscores_per_class': meterscores_per_class,
                   'profile_image_url': get_profile_image_url(user, settings.PASSWORD_FOLDER)})

def results_overview(request,user):

    user = figure_out_username_capitalization(user)

    if user in [None,'']:
        return HttpResponse('Er is een probleem. Heb je misschien een afgeschermd account?')

    return render(request,'result_overview.html',{'twitter_user':user,
                                                  'classifier_sections':ClassifierSection.objects.all().order_by('position'),
                                                  'profile_image_url':get_profile_image_url(user,settings.PASSWORD_FOLDER )})

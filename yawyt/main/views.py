from django.shortcuts import render
from django.http import HttpResponse
from main.models import ClassifierSection
import yawyt.settings as settings
from main.twitterlib.tweet import file_to_tweet_dict, add_annotations_in_files_to_tweets
from main.twitterlib.profile_image import get_profile_image_url
from main.analysis import start_analysis_thread_for_user

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

    most_extreme_tweets = {}

    #Add the annotations for all classifiers
    for classifier_section in ClassifierSection.objects.all():

        classifier_name = classifier_section.classifier_module_name
        add_annotations_in_files_to_tweets(settings.CLASSIFICATION_DATAFOLDER+user+'.'+classifier_name+'.txt',classifier_name,all_tweets_for_user)

        #Prepare saving the most extreme scores for each class for this classifier
        most_extreme_tweets[classifier_name] = {}

        #See what classes there are for this classifier, by taking them from a random tweet
        classes_for_this_classifier = all_tweets_for_user[all_tweets_for_user.keys()[0]].automatic_classifications[classifier_name].keys()

        #For each class, take the most extreme cases
        for classname in classes_for_this_classifier:
            all_tweets_sorted_by_score_for_this_class = sorted(all_tweets_for_user.values(),key=lambda tweet: tweet.automatic_classifications[classifier_name][classname])
            most_extreme_tweets[classifier_name][classname] = all_tweets_sorted_by_score_for_this_class[:settings.NUMBER_OF_TWEETS_TO_SHOW_PER_CLASS]

        print(most_extreme_tweets)

    return render(request,'result_overview.html',{'classifier_sections':ClassifierSection.objects.all().order_by('position'),
                                                  'most_extreme_tweets':most_extreme_tweets,
                                                  'profile_image_url':get_profile_image_url(user,settings.PASSWORD_FOLDER )})

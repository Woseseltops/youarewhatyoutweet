from django.shortcuts import render
from django.http import HttpResponse
from models import ClassifierSection
import yawyt.settings as settings
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

    return render(request,'result_overview.html',{'classifier_sections':ClassifierSection.objects.all()})
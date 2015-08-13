from django.shortcuts import render
from django.http import HttpResponse
from models import ClassifierSection

# Create your views here.

def twittername_entry(request):
    return render(request,'twittername_entry.html')

def analyze(request):
    return render(request,'analyze.html')

def results(request):

    return render(request,'result_overview.html',{'classifier_sections':ClassifierSection.objects.all()})

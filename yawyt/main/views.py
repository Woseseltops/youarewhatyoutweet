from django.shortcuts import render
from django.http import HttpResponse
from models import ClassifierSection

# Create your views here.

def index(request):

    return render(request,'main.html',{'classifier_sections':ClassifierSection.objects.all()})

from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
# Create your views here.

def index(request):
    context = {
        "tweets": Tweet.objects.all()
    }
    return render(request, "index.html", context) #renders from the templates folder in the app folder


def textresponse(request):
    return HttpResponse("Oh hello")
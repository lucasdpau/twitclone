from django.contrib.auth import authenticate, login, logout #import djangos builtin authentication library
from django.contrib.auth.models import User              #Allows us to create users and save to the DB
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Tweet, Profile
# Create your views here.

def index(request):
    #i used to commented out region to run code, to go through existing users and update the db so that they would have a profile attached
    #users = User.objects.all()
    #for user in users:
        #profile = Profile.objects.filter(user=user)
        #if profile.count() < 1:
            #Profile.objects.create(user=user) 
    if not request.user.is_authenticated:
        return render(request, "login.html", {}) #renders from the templates folder in the app folder
    current_username = request.user.username  
    # add all queried objects to a list
    tweetlist = []
    for items in Tweet.objects.all():
        tweetlist.append(items)
    #reverse the list so that the latest tweets are on top
    tweetlist.reverse()
    if len(tweetlist) > 5:
        tweetlist = tweetlist[:5]
    authenticated_username = request.user.username
    return render(request, "index.html", {"tweets": tweetlist, "current_username":current_username})

def login_view(request):  #if we name this function 'login', it will be the same as the imported login function so it won't work.
    #If a HTTP POST request is made
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) #Django has built in logout and login functions, so we dont have to code it manually like in flask
            return HttpResponseRedirect(reverse("index"))  # reverses the urlname back to url, so that from the name index we get the url.
        
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})
    #Else if a HTTP GET request is made
    else:
        return render(request, "login.html")
    
def logout_view(request):
    #Django has built in logout and login functions, so we dont have to code it manually like in flask
    logout(request)
    return render(request, "login.html", {"message":"Logged out."})
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        if len(username) == 0:
            return render(request, "register.html", {"message": "Please enter a username"})
        elif len(email) == 0:
            return render(request, "register.html", {"message": "Please enter an email"})
        elif len(password) == 0:
            return render(request, "register.html", {"message": "Please enter a password"})
        elif len(confirm) == 0:
            return render(request, "register.html", {"message": "Please confirm the password"})
        
        if password == confirm:
            #check if username is taken
            check_username = User.objects.filter(username=username)
            if check_username:
                return render(request, "register.html", {"message": "Username taken!"})
            #if not taken creates entry in user db
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return render(request, "login.html")
        else:
            return render(request, "register.html", {"message": "Passwords don't match"})
    #if GET request
    else:
        return render(request, "register.html")

def settings_view(request):
    #TODO this feature is bugged, django is unable to locate user.profile, and thus user.profile.bio . relearn the database before fixing this.
    current_user = request.user.username
    profile_pic = User.objects.get(username=current_user).profile.profile_pic
    profile_url = "app1/" + profile_pic
    if request.method == "POST":
        bio_text = request.POST.get("bio")
        updated_profile_pic = request.POST.get("profile_pic")
        if bio_text:
            if len(bio_text) <= 300:
                current_user_db_row = User.objects.get(username=current_user)
                current_user_db_row.profile.bio = bio_text
                current_user_db_row.save()
        if updated_profile_pic:
            current_user_db_row = User.objects.get(username=current_user)
            current_user_db_row.profile.profile_pic = updated_profile_pic
            current_user_db_row.save() 
    
    return render(request, "settings.html", {"current_user":current_user, "profile_url":profile_url})
    
    
def profile_view(request, profile_name):
    if request.method == "POST":  #if a form has been submitted then we add it to the database
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140:
            new_tweet = Tweet(text=tweet_text, author=request.user)
            new_tweet.save()
    current_username = request.user.username
    if profile_name == current_username:
        is_own_profile = True
    else:
        is_own_profile = False
    #filter so that only tweets by the profile_name are shown
    tweets = Tweet.objects.filter(author__username=profile_name)
    tweet_list = []
    for items in tweets:
        tweet_list.append(items)
    tweet_list.reverse()
    profile_bio = User.objects.get(username=profile_name).profile.bio #TODO Bio can't be found if no profile bio, default doesnt work on test!
    profile_pic = User.objects.get(username=profile_name).profile.profile_pic
    return render(request, "profile.html", {"profile_name": profile_name, "tweets":tweet_list, "current_username":current_username, "is_own_profile":is_own_profile, "profile_bio":profile_bio, "profile_pic":profile_pic })

def reply_view(request, tweet_id):
    #tweet_id is the int in the url reply/<int:tweet_id>
    parent = tweet_id
    parent_tweet = Tweet.objects.filter(id=tweet_id)[0]
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140:
            new_tweet = Tweet(text=tweet_text, author=request.user, parent_tweet=parent)
            new_tweet.save()
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "reply.html", {"tweet_id": parent, "parent_tweet": parent_tweet})

def tweet_view(request, tweet_id):   # tweet_id from path <int:tweet_id> in urls.py
    return_string = str(tweet_id)
    tweet = Tweet.objects.get(id=tweet_id)
    parent_tweet = Tweet.objects.filter(id=tweet.parent_tweet)
    #get all tweets who have their parent tweet as this tweet.
    child_tweets = Tweet.objects.filter(parent_tweet=tweet_id)   
    return render(request, "tweet.html", {"tweet_text": tweet.text, "tweet_author": tweet.author, "tweet_datetime": tweet.datetime, 
                                          "child_tweets": child_tweets, "parent_tweet": parent_tweet, "tweet_id":tweet_id}) 
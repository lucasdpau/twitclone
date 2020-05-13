from django.contrib.auth import authenticate, login, logout #import djangos builtin authentication library
from django.contrib.auth.models import User              #Allows us to create users and save to the DB
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Tweet, Profile, Tags
import datetime
import string

# functions here.
def parse_time(tweet_obj):
    # calculates time between now and the time of a tweet_object's posting
    now = datetime.datetime.now(datetime.timezone.utc)
    time_diff = now - tweet_obj.datetime      #time diff only keeps track of days/seconds and microseconds
    if time_diff.days < 1:
        if time_diff.seconds <= 3600: #if less than 1 hour has passed since the post
            time_diff_mins = int(time_diff.seconds/60)
            tweet_obj.datetime = str(time_diff_mins) + "m"
        else:
            time_diff_hrs = int(time_diff.seconds/3600)
            tweet_obj.datetime = str(time_diff_hrs) + "h"

def get_tags(tweet_text):
    prepared_text = (tweet_text + " ").lower()
    tag_found = False
    tag_list = []
    current_tag = ""
    for character in prepared_text:
        if tag_found:
            if character == " " or character in string.punctuation:
                tag_found = False
                tag_list.append(current_tag)
            else:
                current_tag += character
        else:
            if character == "#":
                tag_found = True
                current_tag = ""
    return tag_list

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
    current_user = request.user
    current_username = request.user.username  
    # add all queried objects to a list
    tweetlist = []
    for items in Tweet.objects.all():
        if not items.is_deleted:
            tweetlist.append(items)
    #reverse the list so that the latest tweets are on top
    tweetlist.reverse()
    if len(tweetlist) > 5:
        tweetlist = tweetlist[:5]
    authenticated_username = request.user.username
    for tweet in tweetlist:
        parse_time(tweet)
            
    return render(request, "index.html", {"tweets": tweetlist, "current_user": current_user, "current_username":current_username})

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
    current_username = request.user.username
    user_model_object = User.objects.get(username=current_username)
    profile_pic = user_model_object.profile.profile_pic
    profile_url = "app1/" + profile_pic
    profile_location = user_model_object.profile.location
    profile_bio = user_model_object.profile.bio
    profile_date_joined = user_model_object.date_joined
    if request.method == "POST":
        bio_text = request.POST.get("bio")
        location_text = request.POST.get("location")
        updated_profile_pic = request.POST.get("profile_pic")
        if bio_text:
            if len(bio_text) <= 300:
                user_model_object.profile.bio = bio_text
                user_model_object.save()
        if location_text:
            if len(location_text) <= 60:
                user_model_object.profile.location = location_text
                user_model_object.save()
        if updated_profile_pic:
            user_model_object.profile.profile_pic = updated_profile_pic
            user_model_object.save()
    
    return render(request, "settings.html", {"current_username":current_username, "profile_url":profile_url, "profile_location": profile_location, "profile_bio": profile_bio, "profile_date_joined": profile_date_joined  })
    
    
def profile_view(request, profile_name):
    # NOTE: the tweet form in index has a POST route to this view.
    if request.method == "POST":  #if a form has been submitted then we add it to the database
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140:
            new_tweet = Tweet(text=tweet_text, author=request.user)
            tweet_tag_list = get_tags(tweet_text)
            new_tweet.save()
            for tags in tweet_tag_list:
                existing_tag = Tags.objects.filter(tagname=tags)
                if existing_tag:
                    existing_tag[0].tweets.add(new_tweet)
                else:
                    new_tag = Tags(tagname=tags)
                    new_tag.save()
                    new_tag.tweets.add(new_tweet)
#TODO check tags, create if a new one is made, save it. then associate the two
        else:
            return HttpResponse("Char limit of 140 exceeded")
    current_user = request.user
    current_username = request.user.username
    if profile_name == current_username:
        is_own_profile = True
    else:
        is_own_profile = False
    #filter so that only tweets by the profile_name are shown
    tweets = Tweet.objects.filter(author__username=profile_name)
    tweet_list = []
    for items in tweets:
        if not items.is_deleted:
            tweet_list.append(items)
    tweet_list.reverse()
    for tweet in tweet_list:
        parse_time(tweet)
    user_model_object = User.objects.get(username=profile_name)
    profile_bio = user_model_object.profile.bio #TODO Bio can't be found if no profile bio, default doesnt work on test!
    profile_pic = user_model_object.profile.profile_pic
    profile_location = user_model_object.profile.location
    profile_date_joined = user_model_object.date_joined
    return render(request, "profile.html", { "current_user": current_user, "profile_name": profile_name, "tweets":tweet_list, "current_username":current_username, "is_own_profile":is_own_profile, "profile_bio":profile_bio, "profile_pic":profile_pic, "profile_location":profile_location, "profile_date_joined": profile_date_joined })

def reply_view(request, tweet_id):
    current_username = request.user.username
    #tweet_id is the int in the url reply/<int:tweet_id>
    parent = tweet_id
    parent_tweet = Tweet.objects.filter(id=tweet_id)[0]
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140:
            new_tweet = Tweet(text=tweet_text, author=request.user, parent_tweet=parent)
            tweet_tag_list = get_tags(tweet_text)
            new_tweet.save()
            for tags in tweet_tag_list:
                existing_tag = Tags.objects.filter(tagname=tags)
                if existing_tag:
                    existing_tag[0].tweets.add(new_tweet)
                else:
                    new_tag = Tags(tagname=tags)
                    new_tag.save()
                    new_tag.tweets.add(new_tweet)
            parent_tweet.replies += 1
            parent_tweet.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Char limit of 140 exceeded")
    
    return render(request, "reply.html", {"current_username": current_username, "tweet_id": parent, "tweet": parent_tweet})

def tweet_view(request, tweet_id):   # tweet_id from path <int:tweet_id> in urls.py
    current_username = request.user.username
    return_string = str(tweet_id)
    tweet = Tweet.objects.get(id=tweet_id)
    parent_tweet = Tweet.objects.filter(id=tweet.parent_tweet)
    #get all tweets who have their parent tweet as this tweet.
    child_tweets = Tweet.objects.filter(parent_tweet=tweet_id)   
    return render(request, "tweet.html", {"current_username": current_username, "tweet":tweet, "tweet_text": tweet.text, 
                                          "child_tweets": child_tweets, "parent_tweet": parent_tweet, "tweet_id":tweet_id}) 

def delete_tweet(request, tweet_id):
    tweet = Tweet.objects.filter(id=tweet_id)[0]
    if request.user.username == tweet.author.username:
        tweet.deleted_text = tweet.text
        tweet.is_deleted = True
        tweet.text = "[Deleted]"
        tweet.save()
        return HttpResponse("Deletion succesful.")
    else:
        return HttpResponse("You are not the author of this tweet.")

def tag_view(request, tag_name):
    current_user = request.user
    posts = Tweet.objects.filter(tags__tagname=tag_name)
    tweet_list = []
    for tweets in posts:
        tweet_list.append(tweets)
    tweet_list.reverse()
    return render(request, "tags.html", { "posts": tweet_list, "current_username": current_user.username, })
    
    
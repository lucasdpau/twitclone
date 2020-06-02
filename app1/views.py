from django.contrib.auth import authenticate, login, logout #import djangos builtin authentication library
from django.contrib.auth.models import User              #Allows us to create users and save to the DB
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Tweet, Profile, Tags
import datetime
import string

# functions here.
def parse_time(tweet_obj):
    # calculates time between now and the time of a tweet_object's posting
    now = datetime.datetime.now(datetime.timezone.utc)
#the object from datetime only keeps track of days, seconds and microseconds, so we must work aroudn these units
    time_diff = now - tweet_obj.datetime    
#twitter truncates times to hours/minutes if a post is recent  
    if time_diff.days < 1:
        if time_diff.seconds <= 3600: #if less than 1 hour has passed since the post
            time_diff_mins = int(time_diff.seconds/60)
            tweet_obj.datetime = str(time_diff_mins) + "m"
        else:
            time_diff_hrs = int(time_diff.seconds/3600)
            tweet_obj.datetime = str(time_diff_hrs) + "h"

def get_tags(tweet_text):
# goes through a string, finds words that start with '#', populates a list with them and returns the list
    prepared_text = (tweet_text + " ").lower()
    tag_found = False
    tag_list = []
    current_tag = ""
    for character in prepared_text:
        if tag_found:
            if character == " " or character in string.punctuation:
                tag_found = False
                if len(current_tag) > 50:
                    pass
                else:
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
    current_user = request.user
    if not current_user.is_authenticated:
        return render(request, "login.html", {}) #renders from the templates folder in the app folder
    current_username = request.user.username  
    current_user_profile = Profile.objects.get(user__username=current_username)
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
    tweets_liked_by_current_user = Tweet.objects.filter(liked_by=current_user_profile)
    tweets_retweeted_by_current_user = Tweet.objects.filter(retweeted_by=current_user_profile)
    for tweet in tweetlist:
        parse_time(tweet)
    #package a list of the tweets tags into the tweet object
        tweet.tag_list = tweet.tags_set.all()
        if tweet in tweets_liked_by_current_user:
            tweet.is_liked_by_current_user = True
        if tweet in tweets_retweeted_by_current_user:
            tweet.is_retweeted_by_current_user = True

    context = {"tweets": tweetlist, "current_user": current_user, "current_username":current_username, 
"logged_in": current_user.is_authenticated}

    return render(request, "index.html", context)

def login_view(request):  #if we name this function 'login', it will be the same as the imported login function so it won't work.
    #If a HTTP POST request is made
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user) #Django has built in logout and login functions, so we dont have to code it manually like in flask
            return HttpResponseRedirect(reverse("index"))  # reverses the urlname back to url, so that from the name index we get the url.
        
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})
    #Else if a HTTP GET request is made
    else:
        return render(request, "login.html")

@login_required 
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
            #if not taken creates entry in user db, then automaticall logs in the user
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                user_login = authenticate(request, username=username, password=password)
                login(request, user_login)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "register.html", {"message": "Passwords don't match"})
    #if GET request
    else:
        return render(request, "register.html")

@login_required
def settings_view(request):
    current_username = request.user.username
    user_model_object = User.objects.get(username=current_username)
    profile_pic = user_model_object.profile.profile_pic
    profile_url = "app1/" + profile_pic
    profile_location = user_model_object.profile.location
    profile_bio = user_model_object.profile.bio
    profile_date_joined = user_model_object.date_joined
    privacy_mode_enabled = user_model_object.profile.is_private
    if request.method == "POST":
        bio_text = request.POST.get("bio")
        location_text = request.POST.get("location")
        privacy_mode = request.POST.get("privacy")
        updated_profile_pic = request.POST.get("profile_pic")
        if bio_text:
            if len(bio_text) <= 300:
                user_model_object.profile.bio = bio_text
                user_model_object.save()
        if location_text:
            if len(location_text) <= 60:
                user_model_object.profile.location = location_text
                user_model_object.save()
        if privacy_mode == None:
            if privacy_mode_enabled:
                user_model_object.profile.is_private = False
                user_model_object.save()
                print("user disabling privacy mode")
        elif privacy_mode == "privacy":
            if privacy_mode_enabled == False:
                user_model_object.profile.is_private = True
                user_model_object.save()
                print("user enabling privacy mode")
        if updated_profile_pic:
            user_model_object.profile.profile_pic = updated_profile_pic
            user_model_object.save()
        return HttpResponseRedirect("settings")
    
    context = {"current_username":current_username, "profile_url":profile_url, 
"profile_location": profile_location, "profile_bio": profile_bio, 
"profile_date_joined": profile_date_joined, "logged_in": True, 
"privacy_mode_enabled": privacy_mode_enabled, }

    return render(request, "settings.html", context)
    
 
def profile_view(request, profile_name):
    # NOTE: the tweet form in index has a POST route to this view.
    if request.method == "POST":  #if a form has been submitted then we add it to the database
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140 and len(tweet_text) > 0:
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
        else:
            return HttpResponse("Char limit of 140 exceeded")

    user_model_object = User.objects.get(username=profile_name)
    profile_pic = user_model_object.profile.profile_pic
    followers = Profile.objects.filter(following=user_model_object.profile)
    follower_count = followers.count()
    following = Profile.objects.filter(followed_by=user_model_object.profile)
    following_count = following.count()
    already_following = False

    #filter so that only tweets by the profile_name are shown
    profile_tweets = Tweet.objects.filter(author__username=profile_name)
    retweets = Tweet.objects.filter(retweeted_by__user=user_model_object)
    tweets = profile_tweets.union(retweets).order_by('datetime')
    tweet_list = []
    for items in tweets:
        if not items.is_deleted:
            tweet_list.append(items)
    tweet_list.reverse()
    if len(tweet_list) > 5:
        tweet_list = tweet_list[:5]
    for tweet in tweet_list:
        parse_time(tweet)
    #package a list of the tweets tags into the tweet object
        tweet.tag_list = tweet.tags_set.all()


    current_user = request.user
    current_username = None
    is_own_profile = False
    if current_user.is_authenticated:
        current_username = request.user.username
        current_user_profile = Profile.objects.get(user__username=current_username)
        tweets_liked_by_current_user = Tweet.objects.filter(liked_by=current_user_profile)
        tweets_retweeted_by_current_user = Tweet.objects.filter(retweeted_by=current_user_profile)
        if profile_name == current_username:
            is_own_profile = True
        if current_user.profile in followers:
            already_following = True
        for tweet in tweet_list:
            if tweet in tweets_liked_by_current_user:
                tweet.is_liked_by_current_user = True
            if tweet in tweets_retweeted_by_current_user:
                tweet.is_retweeted_by_current_user = True


    context = { "logged_in": current_user.is_authenticated, "current_user": current_user, "profile_name": profile_name, 
"tweets":tweet_list, "current_username": current_username, 
"user_object": user_model_object, "is_own_profile": is_own_profile,  
"profile_pic":profile_pic, "followers": followers, 
"already_following": already_following, "follower_count": follower_count,
"following_count": following_count, }

    return render(request, "profile.html", context)


def tweet_view(request, tweet_id):   # tweet_id from path <int:tweet_id> in urls.py
    current_user = request.user
    current_username = None 
    if current_user.is_authenticated:
        current_username = request.user.username
    return_string = str(tweet_id)
    tweet = Tweet.objects.get(id=tweet_id)
    tweet.tag_list = tweet.tags_set.all()
    try:
        parent_tweet = Tweet.objects.get(id=tweet.parent_tweet)
    except:
        parent_tweet = None
    #get all tweets who have their parent tweet as this tweet.
    child_tweets = Tweet.objects.filter(parent_tweet=tweet_id)

    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
# we also don't want empty tweets
        if len(tweet_text) <= 140 and len(tweet_text) > 0:
            new_tweet = Tweet(text=tweet_text, author=request.user, parent_tweet=tweet.id)
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
            tweet.replies += 1
            tweet.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Char limit of 140 exceeded")

    parse_time(tweet)
    context = {"current_username": current_username, "tweet":tweet, 
"tweet_text": tweet.text, "child_tweets": child_tweets, "parent_tweet": parent_tweet, 
"tweet_id":tweet_id, "logged_in": current_user.is_authenticated,}

    return render(request, "tweet.html", context) 


@login_required
def delete_tweet(request, tweet_id):
# we must make sure the logged in user is the same as the tweets author!
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
    current_username = None
    if current_user.is_authenticated:
        current_username = current_user.username
# get all tweets with a certain tag, add them to a list so we can iterate over them in the view
    tweet_list = []
    posts = Tweet.objects.filter(tags__tagname=tag_name, is_deleted=False)
    for tweets in posts:
        tweet_list.append(tweets)
    tweet_list.reverse()
    return render(request, "tweetlist.html", { "posts": tweet_list, "current_username": current_username, "logged_in": current_user.is_authenticated,})
    
@login_required
@csrf_exempt
def retweet(request, tweet_id):
#check if it's been retweeted before. if not, then add it to the profile's retweet list
    if request.method == "GET":
        return HttpResponse("Don't GET this")

    current_user = request.user
    current_user_profile = Profile.objects.get(user__username=current_user.username)
    retweeted_by_current_user = Tweet.objects.filter(retweeted_by=current_user_profile)
    to_be_retweeted = Tweet.objects.get(id=tweet_id)
    retweet_or_undo = request.POST.get("re_or_undo")
    print(retweet_or_undo)
    if to_be_retweeted in retweeted_by_current_user:
        print("this has already been retweeted, undoing retweet")
        current_user_profile.retweets.remove(to_be_retweeted)
        return HttpResponse("Retweet")
    elif retweet_or_undo == "retweet":
        print("retweeting", to_be_retweeted )
        current_user_profile.retweets.add(to_be_retweeted)
        return HttpResponse("Untweet")

    return HttpResponse("boop")

def liked_tweet_view(request, profile_name):
# returns a list of tweets liked by <profile_name>
    current_user = request.user
    tweets_liked_by_profile = Tweet.objects.filter(liked_by__user__username=profile_name).all()
    for tweet in tweets_liked_by_profile:
        tweet.tag_list = tweet.tags_set.all()

    context = { "posts": tweets_liked_by_profile, "current_username": current_user.username, 
"logged_in": current_user.is_authenticated, }

    return render(request, "tweetlist.html", context)


@csrf_exempt
def follow_view(request, profile_name):
  #check if current_user_profile is following profile_name, if not then add to db.
    current_user = request.user
    if current_user.is_authenticated:
        if request.method == 'POST':
            current_user_profile = Profile.objects.get(user__username=current_user.username)
            users_followed_by_current_user = Profile.objects.filter(followed_by=current_user_profile)
            user_tobe_followed = Profile.objects.get(user__username=profile_name)
            if user_tobe_followed in users_followed_by_current_user:
                print("already following {}".format(profile_name))
                current_user_profile.following.remove(user_tobe_followed)
# we return the text "follow" so that the javascript knows what to replace the button label with.
                return HttpResponse("Follow")
            else:
                print("not x, so now you follow {}".format(profile_name))
                current_user_profile.following.add(user_tobe_followed) 
                return HttpResponse("Unfollow")
            return HttpResponse("Error")

        elif request.method == "GET":
            user_profile = Profile.objects.get(user__username=profile_name)
            users_followed_by_user = user_profile.following.all()
            followers_of_user = Profile.objects.filter(following=user_profile)
            list_of_followers = []
            list_of_followed_by_user = []
            for users in users_followed_by_user:
                list_of_followed_by_user.append(users.user.username)
            for users in followers_of_user:
                list_of_followers.append(users.user.username)
            follow_json = {}
            follow_json["followers"] = list_of_followers
            follow_json["following"] = list_of_followed_by_user

            return JsonResponse(follow_json)

        else:
            return HttpResponse("No")
    else:
        return HttpResponse("NotLoggedIn")

@csrf_exempt
def like_unlike(request, tweet_id):
    current_user = request.user
    if current_user.is_authenticated:
# we only allow likes for logged in users. 
        current_user_profile = Profile.objects.get(user__username=current_user.username)
        tweets_liked_by_current_user = Tweet.objects.filter(liked_by=current_user_profile)
        if request.method == 'POST':
            like_or_unlike = request.POST.get("likeunlike")
            print(like_or_unlike, request.POST)
            current_tweet = Tweet.objects.get(id=tweet_id)
            if current_tweet in tweets_liked_by_current_user and like_or_unlike == "unlike":
                print('removing')
                current_user_profile.liked_tweets.remove(current_tweet)
# we return the response "like" so that the javascript knows to change the button back to like
                return HttpResponse("Like")

            elif not current_tweet in tweets_liked_by_current_user and like_or_unlike == "like":
                print('adding')
                current_user_profile.liked_tweets.add(current_tweet)
                return HttpResponse("Unlike")

            else:
                print('error, nothing saved to db')
            return HttpResponse("yes")
        else:
            response = {"tweets_liked_by_current_user":[]}
            for tweets in tweets_liked_by_current_user:
                response["tweets_liked_by_current_user"].append(tweets.text)
            return JsonResponse(response)
    else:
        return HttpResponse("NotLoggedIn")

def users_view(request):
    current_user = request.user
    all_users = User.objects.all()
    user_list = []
    for item in all_users:
        item.profile.follower_count = item.profile.followed_by.count()
        item.profile.following_count = item.profile.following.count()
#we don't want to count the deleted tweets
        item.profile.tweet_count = Tweet.objects.filter(author=item).exclude(is_deleted=True).count()
        user_list.append(item)
    json_response = {"userlist":user_list}
    print(json_response)
    return render(request, "users.html", {"user_list": user_list, "logged_in": current_user.is_authenticated, "current_username": current_user.username })

@login_required
def followed_users_view(request):
    current_user = request.user
    current_user_profile = Profile.objects.get(user__username=current_user.username)
    user_list = []
    followed_users = User.objects.filter(profile__followed_by=current_user_profile).all()
    for item in followed_users:
        user_list.append(item)
    context = {"user_list": user_list, "logged_in": current_user.is_authenticated, 
"current_username": current_user.username, }
    return render(request, "users.html", context)    


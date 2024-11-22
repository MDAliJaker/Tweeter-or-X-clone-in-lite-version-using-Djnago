from django.shortcuts import render, redirect 
from . models import Profile, tweets
from django.contrib import messages
from .forms import TweetForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                Tweet = form.save(commit=False)
                Tweet.user = request.user
                Tweet.save()
                messages.success(request,("Your Tweet Has Been Posted!") )
                return redirect('home')
        Tweets = tweets.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'Tweets':Tweets, "form":form})
    else:
        Tweets = tweets.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'Tweets':Tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request,("You Must Be Logged in to See that page") )
        return redirect('home')

def profile(request, pk):
     profile = Profile.objects.get(user_id=pk)
     Tweets = tweets.objects.filter(user_id=pk).order_by("-created_at")


     if request.user.is_authenticated:
        
         if request.method == "POST":
             
             current_user_profile = request.user.profile
             action = request.POST['follow']

             if action == "unfollow" :
                 current_user_profile.follows.remove(profile)

             elif action == "follow" :
                 current_user_profile.follows.add(profile)

             current_user_profile.save() 

         return render(request, "profile.html", {"profile":profile, 'Tweets':Tweets})
     else:
        messages.success(request,("You Must Be Logged in to See that page") )
        return redirect('home')
     

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You Have been Login, Happy Tweeting ;) ") )
            return redirect('home')
        else:
             messages.success(request,("There was an error :( Please Try again... ") )
             return redirect('login')
    else:    
        
        return render(request, "login.html", {})


def logout_user(request):    
    logout(request)
    messages.success(request,("Sad to see you go '_' , wanna login again!!") )
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password  = form.cleaned_data['password1']

            user=authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("You have successfully registeed. Wellcome!") )
            return redirect('home')
            
    return render(request, "register.html", {'form':form})


def update_user(request):
    if request.user.is_authenticated:
         current_user = User.objects.get(id=request.user.id)
         user_form = SignUpForm(request.POST or None, instance=current_user)
         if user_form.is_valid():
             user_form.save()
             login(request, current_user)
             messages.success(request,("Your Profile has been Updated") )
             return redirect('home')
         return render(request, "update_user.html", {'form':user_form})
    else:
        messages.success(request,("You Must Be Logged in to See that page") )    
        return redirect('home')
   
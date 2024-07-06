from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from chats.models import DirectChat


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("users:friends")
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect("users:login")
    else:
        return render(request, "auth/login.html", {})


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)
        return redirect("chats:index")
    else:
        return render(request, "auth/register.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out properly"))
    return redirect("users:login")


@login_required
def friends(request):
    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        profile = profiles.first()
    else:
        logout(request)
        messages.success(request, ("Please use different account"))
        return redirect("users:login")
    potential_friends = list(Profile.objects.all())
    friends = list(profile.friends.all())
    for friend in friends:
        if friend in potential_friends:
            potential_friends.remove(friend)

    # I assume you can't talk to yourself
    try:
        potential_friends.remove(profile)
    except:
        friends.remove(profile)

    return render(
        request,
        "users/friends.html",
        {"potential_friends": potential_friends, "friends": friends},
    )


@login_required
def add_friend(request, friend_id):
    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        profile = profiles.first()
    else:
        logout(request)
        messages.success(request, ("Please use different account"))
        return redirect("users:login")
    profile.friends.add(Profile.objects.get(id=friend_id))

    return redirect("users:friends")


@login_required
def remove_friend(request, friend_id):
    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        profile = profiles.first()
    else:
        logout(request)
        messages.success(request, ("Please use different account"))
        return redirect("users:login")
    profile.friends.remove(Profile.objects.get(id=friend_id))

    return redirect("users:friends")


def start_chat(request, friend_id):
    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        profile = profiles.first()
    else:
        logout(request)
        messages.success(request, ("Please use different account"))
        return redirect("users:login")
    profile2 = Profile.objects.get(id=friend_id)
    # we want to test whether chat already exist
    test_set = DirectChat.objects.filter(profiles=profile)
    test_set2 = DirectChat.objects.filter(profiles=profile2)
    final_set = test_set & test_set2
    if final_set.exists():
        room_name = final_set.first().id
        return redirect("chats:room_name", room_name=room_name)

    dc = DirectChat.objects.create()
    dc.profiles.add(profile, profile2)
    return redirect("chats:room_name", room_name=dc.id)

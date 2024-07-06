from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DirectChat
from django.contrib import messages
from users.models import Profile
from django.contrib.auth import logout


# Create your views here.
@login_required
def index(request):
    return redirect("users:friends")


@login_required
def room(request, room_name):
    chats = DirectChat.objects.filter(id=room_name)
    if chats.exists():
        chat = chats.first()
    else:
        messages.success(request, "This chat does not exsist")
        return render(request, "chats/error.html", {})
    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        profile = profiles.first()
    else:
        logout(request)
        messages.success(request, ("Please use different account"))
        return redirect("users:login")
    if not chat.profiles.filter(pk=profile.pk).exists():
        messages.success(request, "This is not your chat, please use different account")
        return render(request, "chats/error.html", {})
    return render(request, "chats/room.html", {"room_name": room_name})

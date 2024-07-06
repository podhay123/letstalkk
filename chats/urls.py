from django.urls import path
from . import views


app_name = "chats"

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:room_name>/", views.room, name="room_name"),
]

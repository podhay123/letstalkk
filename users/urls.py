from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login_user/", views.login_user, name="login"),
    path("register_user/", views.register_user, name="register"),
    path("logout_user/", views.logout_user, name="logout"),
    path("friends/", views.friends, name="friends"),
    path("add_friend/<int:friend_id>/", views.add_friend, name="add_friend"),
    path("remove_friend/<int:friend_id>/", views.remove_friend, name="remove_friend"),
    path("start_chat/<int:friend_id>/", views.start_chat, name="start_chat"),
]

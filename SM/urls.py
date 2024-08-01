from django.urls import path
from . import views

app_name = "SM"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("post_details/<int:post_id>/", views.post_details, name="post_details"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("user_profile/<int:profile_id>/", views.user_profile, name="user_profile"),
    path(
        "user_profile/add_follower/<int:profile_id>",
        views.add_follower,
        name="user_profile/add_follower",
    ),
    path("edit_profile/<int:profile_id>", views.edit_profile, name="edit_profile"),
    path("upload_img/<int:profile_id>", views.upload_img, name="upload_img"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("settings/<int:profile_id>", views.settings, name="settings"),
    path("users_list/", views.search_user, name="users_list"),
    path(
        "change_password/<int:profile_id>",
        views.change_password,
        name="change_password",
    ),
    path("delete_acc/", views.delete_acc, name="delete_acc"),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Comment, PosLike
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post


# ? Authentication :
# Sign Up Handler
def user_signup(request):
    if request.method == "POST":
        # gathering input data
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        # Validate the password matching
        if password != password2:
            messages.info(request, "Password dose not match!")
            return redirect("SM:signup")
        # Check if user name or email is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "username is already taken!")
            return redirect("SM:signup")
            # create new user
        if User.objects.filter(email=email).exists():
            messages.error(request, "email is already taken!")
            return redirect("SM:signup")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()
        # create new profile
        Profile.objects.create(user=new_user)
        # authenticat , login the user , redirect to the index
        authenticated_user = authenticate(request, username=username, password=password)

        login(request, authenticated_user)
        return redirect("SM:index")
    else:
        return render(request, "signup.html")


# Log In Handler
def user_login(request):
    if request.method == "POST":
        # Get The logged data
        username = request.POST["username"]
        password = request.POST["password"]
        # Validate , authenticate
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("SM:index")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("SM:login")
    else:
        return render(request, "login.html")


# Log out Handler
def user_logout(request):
    logout(request)
    return redirect("SM:login")


# User Change Password
@login_required
def change_password(request, profile_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if profile_id != user.profile.id:
            return HttpResponseForbidden("Not Authorized!")
        else:
            curr_pwd = request.POST.get("current_password")
            auth_user = authenticate(
                request, username=request.user.username, password=curr_pwd
            )

            if not auth_user:
                return render(
                    request,
                    "settings.html",
                    {"profile_id": profile_id, "error": "Incorrect current password."},
                )
            else:
                new_pwd = request.POST.get("new_password")
                confirm_pwd = request.POST.get("confirm_password")

                if new_pwd == confirm_pwd:
                    user.set_password(new_pwd)
                    user.save()
                    return redirect("SM:login")
                else:
                    return render(
                        request,
                        "settings.html",
                        {
                            "profile_id": profile_id,
                            "error": "New passwords do not match.",
                        },
                    )


# Create your views here.
@login_required
def index(request):
    # If post request create new post
    if request.method == "POST":
        author = request.user
        content = request.POST.get("content")
        post_img = request.FILES.get("post_img")

        new_post = Post.objects.create(
            author=author, content=content, post_img=post_img
        )
        new_post.save()

        messages.success(request, "Post Created Successfully!")
        return redirect("SM:index")
    else:
        # post_list = Post.objects.all()
        post_list = []
        user_posts = request.user.posts.all()
        post_list.extend(user_posts)
        followings = request.user.profile.following.all()
        for x in followings:
            post_list.extend(x.posts.all())
        print(post_list)
        post_list.sort(key=lambda post: post.published_at, reverse=True)
        return render(request, "index.html", {"post_list": post_list})


@login_required
def user_profile(request, profile_id):
    is_followed = False
    curr_user = request.user
    profile = get_object_or_404(Profile, id=profile_id)
    user_posts = Post.objects.filter(author=profile.user)
    followers = profile.followers.all()
    followings = profile.following.all()
    no_of_followers = len(followers)
    no_of_followings = len(followings)
    if curr_user in followers:
        is_followed = True

    context_obj = {
        "profile": profile,
        "user_posts": user_posts,
        "no_of_followers": no_of_followers,
        "no_of_followings": no_of_followings,
        "is_followed": is_followed,
    }
    return render(request, "user_profile.html", context_obj)


@login_required
def post_details(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(post=post, author=request.user, content=content)
    comments = post.comments.all()
    return render(request, "post_details.html", {"post": post, "comments": comments})


@login_required
def like_post(request, post_id):
    username = request.user.username
    post_id = post_id
    post = Post.objects.get(id=post_id)

    like_exists = PosLike.objects.filter(post_id=post_id, username=username).exists()
    if not like_exists:
        new_like = PosLike.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        PosLike.objects.filter(post_id=post_id, username=username).delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect(request.META.get("HTTP_REFERER"))


@login_required
def add_follower(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    curr_user = request.user
    if curr_user in profile.followers.all():
        profile.followers.remove(curr_user)
        curr_user.profile.following.remove(profile.user)
        return redirect("SM:user_profile", profile_id=profile_id)
    else:
        profile.followers.add(curr_user)
        curr_user.profile.following.add(profile.user)
        return redirect("SM:user_profile", profile_id=profile_id)


@login_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    context_obj = {"profile": profile}
    return render(request, "edit_profile.html", context_obj)


@login_required
def upload_img(request, profile_id):
    if request.method == "POST":
        img = request.FILES.get("profile_img")
        user = request.user
        profile = get_object_or_404(Profile, id=profile_id)
        # update the profile picture
        if profile.user == request.user:
            user.profile.profile_img = img
            user.save()
            user.profile.save()
            messages.success(request, "Profile Picture Updated Successfully!")
            return redirect("SM:edit_profile", profile_id=profile_id)
        else:
            messages.error(request, "Un Authorized!")
            return redirect("SM:edit_profile", profile_id=profile_id)


# Delete Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    curr_user = request.user
    post_user = post.author

    if curr_user == post_user:
        post.delete()
        messages.success(request, "Post Deleted Successfully!")
        return redirect(request.META.get("HTTP_REFERER", "{% url 'SM:index' %}"))
    else:
        messages.error(request, "Un Authorized!")
        return redirect(request.META.get("HTTP_REFERER"))


# settings
@login_required
def settings(request, profile_id):
    return render(request, "settings.html", {"profile_id": profile_id})


# search a username
@login_required
def search_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            users = User.objects.filter(
                username__startswith=username[0]
            ).select_related("profile")

            context = {"users": users}

            return render(request, "users_list.html", context=context)
        else:
            return redirect("SM:index")
    else:
        return render(request, "users_list.html")


# delete user account
@login_required
def delete_acc(request):
    user_to_delete = User.objects.get(username=request.user)
    user_to_delete.delete()
    return redirect("SM:index")


#

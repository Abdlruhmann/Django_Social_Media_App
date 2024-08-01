from django.db import models
from django.contrib.auth.models import User


# Path to user posts' files upload
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/post_files/<filename>
    return f"user_{instance.author.id}/post_files/{filename}"


# Create your models here.


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=150, blank=True)
    profile_img = models.ImageField(upload_to="profile_pics", default="default.jpg")
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return self.nick_name


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", db_index=True
    )
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_img = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    no_of_likes = models.IntegerField(verbose_name="no_of_likes", default=0)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:10]}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", db_index=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class PosLike(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return f"post like , for {self.post_id} {self.username}"

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class User(AbstractUser):
    is_moder = models.BooleanField(default=False)
    nwarns = models.IntegerField(default=0)
    # count of warns
    team_rating = models.IntegerField(default=0)
    # user rating as team member
    author_rating = models.IntegerField(default=0)
    # user rating as author
    reg_ip = models.GenericIPAddressField(null=True)
    last_ip = models.GenericIPAddressField(null=True)
    # ip addresses store as str
    date_of_birth = models.DateField(null=True)
    verified = models.BooleanField(default=False)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255)
    # Format: they/them/pronunciation
    parts_access = models.CharField(max_length=255, default='1111111')
    # Contains string with 0 and 1 each of which means an ability of profile parts to be seen
    hard_skills = models.TextField(null=True)
    work_place = models.TextField(null=True)
    education = models.TextField(null=True)


class Punishments(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='punished_user')
    date = models.DateTimeField()
    executor = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='punishing_executor')
    type = models.IntegerField()
    # type of punishment, 0-ban, 1-warn, 2-ip ban, 3-mute
    term = models.DateTimeField(default=None)
    # if exists
    reason = models.CharField(max_length=255)


class StaffPunishments(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='user')
    date = models.DateTimeField()
    executor = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='executor')
    type = models.IntegerField()
    term = models.DateTimeField(default=None)
    # if exists
    reason = models.CharField(max_length=255)


class Post(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    comment_type = models.IntegerField()
    # type of comment, 0-anonymous, 1-not anonymous
    likes = models.IntegerField()
    dislikes = models.IntegerField()


class PostMedia(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/images/%Y/%m/%d',
                              null=True)
    audio = models.FileField(upload_to='post/audios/%Y/%m/%d/',
                             null=True)
    video = models.FileField(upload_to='post/videos/%Y/%m/%d/',
                             null=True)
    file = models.FileField(upload_to='post/files/%Y/%m/%d/',
                            null=True)


class Comment(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    likes = models.IntegerField()
    dislikes = models.IntegerField()


class CommentElement(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    type = models.IntegerField()
    # type of element, 0-text, 1-image, 2-media
    text = models.TextField()
    media = models.CharField(max_length=255)

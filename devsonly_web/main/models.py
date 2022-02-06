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


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    sex = models.IntegerField()
    preposition = models.CharField(max_length=255)


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
    # type of punishment, 0-ban, 1-warn, 2-ip ban, 3-mute
    term = models.DateTimeField(default=None)
    # if exists
    reason = models.CharField(max_length=255)

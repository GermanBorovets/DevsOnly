from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_moder = models.BooleanField(default=False)
    nwarns = models.IntegerField(default=0)
    # count of warns
    is_banned = models.BooleanField(default=False)
    unban_date = models.DateTimeField(null=True)
    team_rating = models.IntegerField(default=0)
    # user rating as team member
    author_rating = models.IntegerField(default=0)
    # user rating as author
    reg_ip = models.GenericIPAddressField(null=True)
    last_ip = models.GenericIPAddressField(null=True)
    # ip addresses store as str
    date_of_birth = models.DateField(null=True)
    verified = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    unmute_date = models.DateTimeField(null=True)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='photos/%Y/%m/%d/', default='photos/def/def.png')
    status = models.CharField(max_length=255, blank=True)
    sex = models.CharField(max_length=255)
    # Format: they/them/pronunciation
    parts_access = models.CharField(max_length=255, default='1111111')
    # Contains string with 0 and 1 each of which means an ability of profile parts to be seen
    # Access by indexes: 0 - date_of_birth, 1 - profile_picture, 2 - status, 3 - sex, 4 - hard_skills
    # 5 - work_place, 6 - education
    work_place = models.TextField(blank=True)
    education = models.TextField(blank=True)


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

    # Clearing storage on delete
    def delete(self, *args, **kwargs) -> None:
        if self.image:
            storage = self.image.storage
            path = self.image.path
        if self.audio:
            storage = self.audio.storage
            path = self.audio.path
        if self.video:
            storage = self.video.storage
            path = self.video.path
        if self.file:
            storage = self.file.storage
            path = self.file.path

        super().delete(*args, **kwargs)
        storage.delete(path)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    created = models.DateTimeField()


class CommentElement(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comment/images/%Y/%m/%d',
                              null=True)
    audio = models.FileField(upload_to='comment/audios/%Y/%m/%d',
                              null=True)
    video = models.FileField(upload_to='comment/videos/%Y/%m/%d',
                             null=True)
    file = models.FileField(upload_to='comment/files/%Y/%m/%d',
                            null=True)


class HardSkills(models.Model):
    tag = models.CharField(max_length=255)


class UserSkills(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    skill = models.ForeignKey(to=HardSkills, on_delete=models.CASCADE)


class BannedIPs(models.Model):
    IP = models.CharField(max_length=15)

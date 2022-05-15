from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ## If user is moderator
    is_moder = models.BooleanField(default=False)
    ## If user is muted
    is_muted = models.BooleanField(default=False)
    ## Date of unmute of user (if it is muted)
    unmute_date = models.DateField(null=True)
    ## Count of warns to user
    nwarns = models.IntegerField(default=0)
    ## User rating as team member
    team_rating = models.IntegerField(default=0)
    ## user rating as author
    author_rating = models.IntegerField(default=0)
    ## User registration ip, store as str
    reg_ip = models.GenericIPAddressField(null=True)
    ## User last ip, store as str
    last_ip = models.GenericIPAddressField(null=True)
    ## Birth date
    date_of_birth = models.DateField(null=True)
    ## If user verificated
    verified = models.BooleanField(default=False)


class UserSettings(models.Model):
    ## Foreign key to User model
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    ## Profile picture of user
    profile_picture = models.ImageField(upload_to='photos/%Y/%m/%d/', default='photos/def/def.png')
    ## User status
    status = models.CharField(max_length=255, blank=True)
    ## User sex (prepositions)
    sex = models.CharField(max_length=255)
    ## Contains string with 0 and 1 each of which means an ability of profile parts to be seen
    ## Access by indexes: 0 - date_of_birth, 1 - profile_picture, 2 - status, 3 - sex, 4 - hard_skills,
    ## 5 - work_place, 6 - education
    parts_access = models.CharField(max_length=255, default='1111111')
    ## Work place
    work_place = models.TextField(blank=True)
    ## Education
    education = models.TextField(blank=True)


class Punishments(models.Model):
    ## Foreign key to user, who get punish
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='punished_user')
    ## Date of punishment
    date = models.DateTimeField()
    ## A person who gives punish
    executor = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='punishing_executor')
    ## type of punishment, 0-ban, 1-warn, 2-ip ban, 3-mute
    type = models.IntegerField()
    ## Reason of punishment
    reason = models.CharField(max_length=255)
    ## Expire date of punishment
    expire_date = models.DateTimeField(null=True)
    # if exists


class StaffPunishments(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='user')
    date = models.DateTimeField()
    executor = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='executor')
    type = models.IntegerField()
    term = models.DateTimeField(default=None)
    # if exists
    reason = models.CharField(max_length=255)


class Post(models.Model):
    ## Text of post
    text = models.TextField(blank=True)
    ## Foreign key to User, author of post
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    ## Date of create
    created = models.DateTimeField()
    ## Date of last modify
    modified = models.DateTimeField()
    ## type of comment, 0-anonymous, 1-not anonymous
    comment_type = models.IntegerField()
    ## Count of likes
    likes = models.IntegerField()
    ## Count of dislikes
    dislikes = models.IntegerField()


class PostMedia(models.Model):
    ## Post which media belongs
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    ## Image field
    image = models.ImageField(upload_to='post/images/%Y/%m/%d',
                              null=True)
    ## Audio field
    audio = models.FileField(upload_to='post/audios/%Y/%m/%d/',
                             null=True)
    ## Video field
    video = models.FileField(upload_to='post/videos/%Y/%m/%d/',
                             null=True)
    ## File field
    file = models.FileField(upload_to='post/files/%Y/%m/%d/',
                            null=True)

    def delete(self, *args, **kwargs) -> None:
        ## Clearing storage on delete
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
    ## Text of comment
    text = models.TextField()
    ## Foreign key to User
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    ## Foreign key to Post
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    ## Count of likes
    likes = models.IntegerField()
    ## Count of dislikes
    dislikes = models.IntegerField()
    ## Date of comment creation
    created = models.DateTimeField()


class CommentElement(models.Model):
    ## Foreign key to Comment
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    ## Image field
    image = models.ImageField(upload_to='comment/images/%Y/%m/%d',
                              null=True)
    ## Audio field
    audio = models.FileField(upload_to='comment/audios/%Y/%m/%d',
                             null=True)
    ## Video field
    video = models.FileField(upload_to='comment/videos/%Y/%m/%d',
                             null=True)
    ## File field
    file = models.FileField(upload_to='comment/files/%Y/%m/%d',
                            null=True)


class HardSkills(models.Model):
    ## Tag of skill
    tag = models.CharField(max_length=255)


class UserSkills(models.Model):
    ## Foreign key to User
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    ## Foreign key to HardSkills
    skill = models.ForeignKey(to=HardSkills, on_delete=models.CASCADE)


class BannedIPs(models.Model):
    ## IPs of banned users
    IP = models.CharField(max_length=15)

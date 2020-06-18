from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=32,blank=True)
    profile_photo = models.ImageField(blank=True,null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.id}'


class FollowerRelation(models.Model):
    follower = models.OneToOneField(User,related_name="follower",on_delete=models.CASCADE)
    followee = models.ManyToManyField(User,related_name="followee")

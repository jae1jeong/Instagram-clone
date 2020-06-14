from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from sorl.thumbnail import images
import datetime

# Create your models here.

class Photo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="timeline_photo/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True) # 수정할때마다 갱신
    like = models.ManyToManyField(User,related_name="like_post",blank=True)
    favorite = models.ManyToManyField(User,related_name="favorite_post",blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        ordering = ['-created'] # created순으로 정렬

    def get_absolute_url(self):
        return reverse("photo:detail",args=[self.id])

class Comment(models.Model):
    photo = models.ForeignKey(Photo,on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_content = models.CharField(max_length=300)

    class Meta:
        ordering = ['-comment_date']


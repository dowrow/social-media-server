from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

UPLOAD_PATH = 'uploads/'


class Publication(models.Model):
    image = models.ImageField(upload_to=UPLOAD_PATH);
    text = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    timestamp = models.DateTimeField(auto_now=True)
    unique_together = ('follower', 'followed',)

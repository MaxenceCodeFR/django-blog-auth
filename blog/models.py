from django.db import models
from django.conf import settings


class Photo(models.Model):

    image = models.ImageField()
    caption = models.TextField(max_length=130, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Blog(models.Model):
    title = models.CharField(max_length=130)
    content = models.CharField(max_length=1500)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, blank=True, null=True)
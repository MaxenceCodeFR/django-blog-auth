from django.db import models
from django.conf import settings
from PIL import Image


class Photo(models.Model):
    IMAGE_MAX_SIZE = (500, 500)

    image = models.ImageField()
    caption = models.TextField(max_length=130, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def resize_image(self):

        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)

        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class Blog(models.Model):
    title = models.CharField(max_length=130)
    content = models.CharField(max_length=1500)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    word_count = models.IntegerField(default=0, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, blank=True, null=True)

    def _get_word_count(self):
        return len(self.content.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)


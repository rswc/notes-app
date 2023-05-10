from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4

# https://stackoverflow.com/a/25768034
@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class User(AbstractUser):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'name']]

    def __str__(self):
        return f'{self.user}: {self.name}'

class Note(models.Model):
    class Colors(models.TextChoices):
        WHITE = 'W', 'White'
        YELLOW = 'Y', 'Yellow'
        GREEN = 'G', 'Green'
        PINK = 'P', 'Pink'

    name = models.CharField(max_length=96)
    content = models.TextField(blank=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    color = models.CharField(
        max_length=1,
        choices=Colors.choices,
        default=Colors.WHITE
    )
    tags = models.ManyToManyField(Tag, related_name='notes')
    public = models.BooleanField(default=False)
    cover = models.ImageField(upload_to=PathAndRename(settings.MEDIA_ROOT), null=True)

    class Meta:
        unique_together = [['owner', 'name']]

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import AbstractUser


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

    class Meta:
        unique_together = [['owner', 'name']]

    def __str__(self):
        return self.name

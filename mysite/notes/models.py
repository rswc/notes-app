from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers


class User(AbstractUser):
    pass

class Note(models.Model):
    name = models.CharField(max_length=96)
    content = models.TextField()
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NoteFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'date_created', 'last_edited']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'date_created', 'last_edited']
        extra_kwargs = {'content': {'write_only': True}}

    def create(self, validated_data):
        note = Note(
            name=validated_data['name'],
            content=validated_data['content'],
            owner=User.objects.get(id=1) #HACK: in the future, read user id from session
        )
        note.save()

        return note

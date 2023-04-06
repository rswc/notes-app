from rest_framework import serializers
from .models import *


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data, 'user': User.objects.get(id=1)}) #self.context['request'].user
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'user']


class NoteFullSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        'name',
        queryset=Tag.objects.filter(user=User.objects.get(id=1)),
        many=True
    )

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'date_created', 'last_edited']

class NoteSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        'name',
        queryset=Tag.objects.filter(user=User.objects.get(id=1)),
        many=True
    )

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


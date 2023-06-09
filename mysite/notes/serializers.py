from rest_framework import serializers
from .models import *


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data, 'user': self.context['request'].user})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')

    def get_queryset(self):
        return self.queryset.filter(user=self.context['request'].user)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class NoteFullSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        'name',
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'date_created', 'last_edited']

class NoteSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        'name',
        queryset=Tag.objects.all(),
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
            owner=self.context['request'].user
        )
        note.save()

        note.tags.set(validated_data['tags'])

        return note
    
    def validate(self, attrs):
        user = self.context['request'].user.id
        name = attrs.get('name')

        if Note.objects.filter(owner=user, name=name).exists():
            raise serializers.ValidationError({'name': ['A note of this title already exists.']})

        return super().validate(attrs)


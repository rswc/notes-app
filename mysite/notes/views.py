from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import *
from .serializers import *


def index(request):
    return render(request, 'landing.html')

class api_notes(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.all()
        # return Note.objects.filter(owner=self.request.user.id)

class api_note(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteFullSerializer
    queryset = Note.objects.all()

class api_tags(generics.ListCreateAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all().order_by('name')
        # return tag.objects.filter(owner=self.request.user.id)

class api_tag(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

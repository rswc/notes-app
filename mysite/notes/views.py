from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import *
from .serializers import *


def index(request, **kwargs):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    return render(request, 'landing.html')

def shared(request, note_id):
    note = get_object_or_404(Note, id=note_id, public=True)

    return render(request, 'shared.html', context={'note': note})

class api_notes(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(owner=self.request.user.id)

        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(name__contains=search) | Q(content__contains=search))

        return queryset

class api_note(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteFullSerializer

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user.id)

class api_tags(generics.ListCreateAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user.id).order_by('name')

class api_tag(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user.id)
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/note/', views.api_notes.as_view(), name='api_notes'),
    path('api/note/<int:pk>/', views.api_note.as_view(), name='api_note'),
]

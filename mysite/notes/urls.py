from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shared/<int:note_id>', views.shared, name='shared'),

    # actual routing is handled by vue
    path('edit/<int:id>', views.index, name='edit'),
    path('create/', views.index, name='create'),
    
    path('api/note/', views.api_notes.as_view(), name='api_notes'),
    path('api/note/<int:pk>/', views.api_note.as_view(), name='api_note'),
    path('api/tag/', views.api_tags.as_view(), name='api_tags'),
    path('api/tag/<int:pk>/', views.api_tag.as_view(), name='api_tag'),
]

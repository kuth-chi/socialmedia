from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.get_notes, name="notes"),
    path('notes/create/', views.create_note, name="create_note"),
    path('notes/<str:pk>/update/', views.update_note, name="update_note"),
    path('notes/<str:pk>/delete/', views.delete_note, name="delete_note"),
    path('notes/<str:pk>/', views.get_note, name="note details"),
    # Shared Note URL pattern
    path('notes/shared/', views.get_notes_shared, name="shared"),

]
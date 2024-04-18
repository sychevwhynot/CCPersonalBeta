from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.feedlist_view, name='feedlist'),
    path('create/', views.create_feed, name='create_feed'),
    path('<int:pk>/edit/', views.edit_feed, name='edit_feed'),
    path('<int:pk>/delete/', views.delete_feed, name='delete_feed'),
]
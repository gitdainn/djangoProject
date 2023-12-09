from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.open_news_youtube, name='youtubeOpenNewsYoutube')
]
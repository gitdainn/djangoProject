from django.urls import path
from . import views
from .views import search_view, get_suggestions


urlpatterns = [
    path('', search_view, name='search_view'),
    path('get_suggestions/', get_suggestions, name='get_suggestions'),
]
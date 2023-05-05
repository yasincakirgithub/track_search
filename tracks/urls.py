from django.urls import path, include
from tracks.views import (search_tracks_page)

urlpatterns = [
    path('', include('tracks.api.urls')),
    path('', search_tracks_page, name='search-track-page')
]

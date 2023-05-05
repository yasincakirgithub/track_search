from django.urls import path
from tracks.api import views as api_views

urlpatterns = [
    path('<genre>',api_views.TrackListAPIView.as_view(), name='get-track-list')
]





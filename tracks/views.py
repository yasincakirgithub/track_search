from django.shortcuts import render


def search_tracks_page(request):
    return render(request, 'tracks/search.html')

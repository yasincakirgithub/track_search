import os
import json
import random
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings


def get_access_token():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    grant_type = 'client_credentials'
    print(client_id, client_secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    url = f"https://accounts.spotify.com/api/token?grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["access_token"]
    else:
        return None


def prepare_track_list(results):
    return [{'artist': result['artists'][0]['name'],
             'track': result['name'],
             'album_image_url': result['album']['images'][0]['url'],
             'preview_url': result['preview_url'],
             } for result in results]


def get_tracks_sorted_by_popularity(access_key, artist, genre):
    result_limit = 10
    limit = 50
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {access_key}'
    }
    url = f"https://api.spotify.com/v1/search?type=track&q=genre:{genre} artist:{artist}&limit={limit}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        results = sorted(response_json["tracks"]["items"], key=lambda d: d['popularity'], reverse=True)[0:result_limit]
        results = prepare_track_list(results)
        return results
    else:
        return None


class TrackListAPIView(APIView):
    def get(self, request, genre):
        datas = []
        genre = genre.lower()
        json_path = os.path.join(settings.STATIC_ROOT, 'tracks', 'genres.json')
        with open(json_path, 'r') as f:
            genre_json = json.load(f)
        if genre in genre_json:
            artist = random.choice(genre_json[genre])
            access_token = get_access_token()
            print("Artist", artist)
            if not access_token:
                return Response({'error': 'access token cannot be created at this time.'},
                                status=status.HTTP_400_BAD_REQUEST)
            datas = get_tracks_sorted_by_popularity(access_token, artist, genre)
            if not datas:
                return Response({'error': 'spotify did not return results'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(datas, status=status.HTTP_200_OK)

import requests
import json
import sys
import config

def artist(artist_name, auth_token):
    """
    Search for an artist in the Spotify catalog, returns that artist information in form of a JSON
    """
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + auth_token}
    params = {'q':artist_name, 'type':'artist'}
    search_req = requests.get(url=url, params=params, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result['artists']['items']
    else:
        return search_req.raise_for_status()


def artist_by_id(artist_id, auth_token):
    """
    Search for an artist in the Spotify catalog using its Spotify ID, 
    returns that artist information in form of a JSON.
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {'Authorization': 'Bearer ' + auth_token}
    search_req = requests.get(url=url, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result
    else:
        return search_req.raise_for_status()


def album(album_name, auth_token, artist_name=''):
    """
    Search for an album in the Spotify catalog,
    returns search results (SimplifiedAlbumObjects) information in form of a JSON.
    If artist name is empty, only search for album name.
    """
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + auth_token}
    
    if artist_name:
        query = f'album:{album_name} artist:{artist_name}'
    else:
        query = f'album:{album_name}'
    params = {'q':query, 'type':'album'}

    search_req = requests.get(url=url, params=params, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result['albums']['items']
    else:
        return search_req.raise_for_status()

def album_by_id(album_id, auth_token):
    """
    Search for an album in the Spotify catalog from its Spotify ID,
    returns search results (AlbumObject) information in form of a JSON.
    """
    url = f'https://api.spotify.com/v1/albums/{album_id}'
    headers = {'Authorization': 'Bearer ' + auth_token}
    
    search_req = requests.get(url=url, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result
    else:
        return search_req.raise_for_status()


def track(track_name, auth_token, artist_name=''):
    """
    Search for that track name from that artist in the Spotify catalog, 
    returns search results (SimplifiedTrackObjects) information in form of a JSON.
    If artist name is empty, only search for track name.
    """
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + auth_token}

    if artist_name:
        query = f'track:{track_name} artist:{artist_name}'
    else:
        query = f'track:{track_name}'
    params = {'q':query, 'type':'track'}
    
    search_req = requests.get(url=url, params=params, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result['tracks']['items']
    else:
        return search_req.raise_for_status()


def track_by_id(track_id, auth_token):
    """
    Get that track id basic information from the Spotify Catalog
    """
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {'Authorization': 'Bearer ' + auth_token}
    
    search_req = requests.get(url=url, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result
    else:
        return search_req.raise_for_status()


def audio_features_by_track_id(track_id, auth_token):
    """
    Get that track audio features information from the Spotify Catalog,
    returns track audio feature (AudioFeaturesObject) information in form of a JSON.
    """
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    headers = {'Authorization': 'Bearer ' + auth_token}
    
    search_req = requests.get(url=url, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result
    else:
        return search_req.raise_for_status()

def audio_analysis_by_track_id(track_id, auth_token):
    """
    Get that track id basic information from the Spotify Catalog
    returns track audio analysis results (AudioAnalysisObject) information in form of a JSON.

    """
    url = f'https://api.spotify.com/v1/audio-analysis/{track_id}'
    headers = {'Authorization': 'Bearer ' + auth_token}
    
    search_req = requests.get(url=url, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result
    else:
        return search_req.raise_for_status()

def get_track_recommendations(auth_token, **kwargs):
    """
    Input kwargs: expected a dictionary of compliant parameters, 
    see https://developer.spotify.com/documentation/web-api/reference-beta/#category-browse
    Recommendations are generated based on the available information for a given seed entity and matched against similar artists and tracks. If there is sufficient information about the provided seeds, a list of tracks will be returned together with pool size details.
    For artists and tracks that are very new or obscure there might not be enough data to generate a list of tracks.
    """

    url = 'https://api.spotify.com/v1/recommendations'
    headers = {'Authorization': 'Bearer ' + auth_token}
    params = kwargs

    search_req = requests.get(url=url, params = params, headers = headers)
    if search_req.ok: 
        result = json.loads(search_req.content)
        return result['tracks'] #skips the seeds part
    else:
        return search_req.raise_for_status()

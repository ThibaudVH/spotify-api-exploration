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


def track(track_name, auth_token, artist_name=''):
    """
    Search for that track name from that artist in the Spotify catalog, 
    returns that artist information in form of a JSON.
    If artist name is empty, only search for track name
    """
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + auth_token}

    if artist_name:
        query = 'track:'+ track_name + ' ' + 'artist:' + artist_name
    else:
        query = 'track:'+ track_name
    params = {'q':query, 'type':'track'}
    
    search_req = requests.get(url=url, params=params, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result['tracks']['items']
    else:
        return search_req.raise_for_status()

def track_by_id(track_id, auth_token):
    """
    Get that track id basic information fromn the Spotify Catalog
    """
    url = 'https://api.spotify.com/v1/tracks'
    headers = {'Authorization': 'Bearer ' + auth_token}
    query = 'ids:'+ track_id
    params = {'q':query}
    
    search_req = requests.get(url=url, params=params, headers = headers)

    if search_req.ok: 
        result = json.loads(search_req.content)
        return result['tracks']
    else:
        return search_req.raise_for_status()
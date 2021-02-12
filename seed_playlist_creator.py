
import numpy as np
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import config

def querify_seed_tracks(seed_file = 'data/seed_tracks.csv'):
    """
    parse the csv of seed tracks and return a query with artist and track names
    @params:
    seed_file       - optional  :   file containing the seed tracks to compose or add to the playlist, default is data/seed_tracks.csv
    """
    
    try:
        with open(seed_file, newline='') as csvfile:
            seed_tracks = csv.DictReader(csvfile)
            seed_querylist=[]
            for row in seed_tracks:
                name = row['name']
                artist = row['artist']
                query = f'track:{name} artist:{artist}'
                seed_querylist.append(query)
        return seed_querylist
    except: 
        "The csv file was not found or could not be parsed"
    
def search_tracks_uri (seed_querylist):
    """
    Search for these tracks in the spotify catalog and get their uri. return a list of Spotify Track URIs
    @params:
    seed_querylist    - Required  : list of queries for tracks to search.
    """

    seed_tracks_uri=[]
    for search_track in seed_querylist:
        result = sp.search(search_track)
        if len(result['tracks']['items'])>0:
            track = result['tracks']['items'][0] # takes first result as default for now
        else:
            print (f'Track not found: {search_track}')
            continue
        artist_names =[]
        for artist in track['artists']: 
            artist_names.append(artist['name'])
        artist_names = ', '.join(artist_names)
        print(track['name'], artist_names)
        seed_tracks_uri.append(track['uri'])
    return seed_tracks_uri

def simple_recommendation_engine(seed_tracks_uri, plist_existing_tracks_uri = None):
    """
    Search for the top 10 recommended songs for each of the seed_tracks, one by one and returns the recommendations' URIs
    @params:
    seed_tracks_uri             - Required  : list of track URIs to get recommendations for.
    plist_existing_tracks_uri   - Optional  : list of track URIs already present in the playlist
    """
    recommended_tracks_uri =[]
    for seed in seed_tracks_uri:
        result = sp.recommendations(seed_tracks=[seed], limit=10)
        for reco in result['tracks']:
            recommended_tracks_uri.append(reco['uri'])
        #     artist_names=[]
        #     for artist in reco['artists']: 
        #         artist_names.append(artist['name'])
        #     artist_names = ', '.join(artist_names)
        #     reco_name = reco['name']
        # # print(f'{reco_name} - {artist_names}')
    #filter recommendations to add based on what's already in the plist
    if plist_existing_tracks_uri:
        recommended_tracks_to_add_uri = np.setdiff1d(recommended_tracks_uri, plist_existing_tracks_uri)
    else:
        recommended_tracks_to_add_uri = recommended_tracks_uri
    return set(recommended_tracks_to_add_uri)

def add_tracks_to_playlist(tracks_to_add, plist_uri):
    """
    Add tracks to a specified playlist. Uses several operation if more than 100 tracks to add.
    @params:
    tracks_to_add           - Required  : list of tracks URIs
    plist_uri               - Required  : playlist URI       
    """
    result=''
    if len(tracks_to_add) > 100:
        floor, remainder = divmod(len(tracks_to_add), 100)
        for i in range(floor):
            result = sp.playlist_add_items(playlist_id=plist_uri, items=tracks_to_add[i:(i+1)*100])
    else:
        result = sp.playlist_add_items(playlist_id = plist_uri, items=tracks_to_add)
    return result

# Initiate os env. variables for spotipy auth
os.environ['SPOTIPY_CLIENT_ID'] = config.authentication['app_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config.authentication['app_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config.authentication['app_redirect_url']

#Initiate Spotipy Client
scope = "user-library-read user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,show_dialog=False))
user_id = sp.me()['id']
print(user_id)

query = querify_seed_tracks()
seed_tracks_uri = search_tracks_uri(query)

plist_name = input('Provide the name of the playlist youd like to create or modify:')
plist_uri=''
plist_existing_tracks_uri=[]
result = sp.current_user_playlists()

for plist in result['items']: #search existing playlist
    if (plist['name'] == plist_name) & (plist['owner']['id'] == user_id):
        plist_uri = plist['uri']
        print('Playlist found in existing user playlists')
        playlist_tracks = sp.playlist_tracks(playlist_id=plist_uri)
        for track in playlist_tracks['items']['tracks']:
            plist_existing_tracks_uri.append(track['uri'])
        break

if not plist_uri: #create playlist
    result = sp.user_playlist_create(user = user_id, name = plist_name, collaborative=True, public = False)
    plist_uri = result['uri']
    print('Playlist created')
print(plist_uri)

#add seed-tracks to playlist
sp_tracks_to_add_uri = np.setdiff1d(seed_tracks_uri, plist_existing_tracks_uri)
result = add_tracks_to_playlist(tracks_to_add = seed_tracks_uri, plist_uri = plist_uri)
print('Seed tracks added to the playlist')

#Get recommendations for each tracks and add to playlist
recommended_tracks_uri = simple_recommendation_engine(seed_tracks_uri, plist_existing_tracks_uri)
result = add_tracks_to_playlist(tracks_to_add = recommended_tracks_uri, plist_uri = plist_uri)
print('recommended tracks added to the playlist')




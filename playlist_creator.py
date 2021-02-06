
import numpy as np
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import config

# Initiate os env. variables for spotipy auth
os.environ['SPOTIPY_CLIENT_ID'] = config.authentication['app_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config.authentication['app_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config.authentication['app_redirect_url']

scope = "user-library-read user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,show_dialog=False))
user_id = sp.me()['id']
print(user_id)

# Import seed tracks and querify them
with open('data/seed_tracks.csv', newline='') as csvfile:
    seed_tracks = csv.DictReader(csvfile)
    seed_tracklist=[]
    for row in seed_tracks:
        name = row['name']
        artist = row['artist']
        query = f'track:{name} artist:{artist}'
        seed_tracklist.append(query)

# Search for these tracks in the spotify catalog and get their uri
seed_tracks_uri=[]
for search_track in seed_tracklist:
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
    seed_tracks_uri.append(track['uri'] )

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
    result = sp.user_playlist_create(user = user_id, name = 'Daytime Rave', collaborative=True, public = False)
    plist_uri = result['uri']
    print('Playlist created')
print(plist_uri)

#add seed-tracks to playlist
sp_tracks_to_add_uri = np.setdiff1d(seed_tracks_uri, plist_existing_tracks_uri)
if len(sp_tracks_to_add_uri)>0:
    result = sp.playlist_add_items(playlist_id = plist_uri, items=seed_tracks_uri)

#Get recommendations for each tracks and put first 10 in the playlist
recommended_tracks_uri =[]
for seed in seed_tracks_uri:
    list_seed = [str(seed)]
    result = sp.recommendations(seed_tracks=[seed], limit=10)
    for reco in result['tracks']:
        recommended_tracks_uri.append(reco['uri'])
        artist_names=[]
        for artist in reco['artists']: 
            artist_names.append(artist['name'])
        artist_names = ', '.join(artist_names)
        reco_name = reco['name']
        # print(f'{reco_name} - {artist_names}')
#filter recommendations to add based on what's already in the plist
recommended_tracks_to_add_uri = np.setdiff1d(recommended_tracks_uri, plist_existing_tracks_uri)
#add recommendations to playlist, max 100 tracks at a time
if len(recommended_tracks_to_add_uri) > 100:
    floor, remainder = divmod(len(recommended_tracks_to_add_uri), 100)
    for i in range(floor):
        result = sp.playlist_add_items(playlist_id=plist_uri, items=recommended_tracks_to_add_uri[i:(i+1)*100])


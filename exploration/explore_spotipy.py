#%%
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import config
#%%
# Initiate os env. variables for spotipy auth
os.environ['SPOTIPY_CLIENT_ID'] = config.authentication['app_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config.authentication['app_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config.authentication['app_redirect_url']

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.me()['id']
print(user_id)
#%%
# Start a client with a defined scope
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#%%
#Get connected user's name
print(sp.me()['display_name'])

#%%
# query via client
results = sp.current_user_saved_tracks()
i=0
for idx, item in enumerate(results['items']):
    if i > 10:
        break
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
    i+=1
    
# %%
# CREATE A FUCKING PLAYLIST RETARD!
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.me()['id']
result = sp.user_playlist_create(user = user_id, name = 'test', public=False, collaborative=False)
print(result)
# %%
#Find tracks
track_name='tunak tunak tun'
artist_name='Mehndi'
query = f'track:{track_name} artist:{artist_name}'
result=sp.search(query)
print(len(result['tracks']['items']))
for track in result['tracks']['items']:
    artist_names =[]
    for artist in track['artists']: 
        artist_names.append(artist['name'])
    artist_names = ', '.join(artist_names)
    print(track['name'], artist_names)

#%%
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp.recommendations()


# %%

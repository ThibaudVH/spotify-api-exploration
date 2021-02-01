
#%%
import json
import csv
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
with open('seed_tracks.csv', newline='') as csvfile:
    seed_tracks = csv.DictReader(csvfile)
    for row in reader:
        print(row)
# %%

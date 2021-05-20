import numpy as np
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError 
import config
import re
import argparse
# from utilities.logutil import getlogger

# logger = getlogger('add_currently_playing')

parser = argparse.ArgumentParser()
parser.add_argument('--playlist', '-p', help = 'the name of the playlist the track should be added to.', required=True)
args = parser.parse_args()
if not args.playlist:
    raise argparse.ArgumentError(message='must provide a non-empty string as playlist name')
plist_name = args.playlist
# Initiate os env. variables for spotipy auth
os.environ['SPOTIPY_CLIENT_ID'] = config.authentication['app_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config.authentication['app_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config.authentication['app_redirect_url']

#Initiate Spotipy Client
scope = "user-library-read user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative app-remote-control streaming user-read-playback-state user-modify-playback-state user-read-currently-playing"
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,show_dialog=False))
    user_id = sp.me()['id']
    # logger.info(f'Succesfully logged in to Spotify as {user_id}')
except SpotifyOauthError as err:
    print(err.__class__.__name__ + ':' + str(err))

# Get current playback
request = sp.current_playback()
if not request:
    print ('No currently playing track.')
    exit()
if (request['item']['type']=='track'):
    track_uri = request['item']['uri']
    track_name = request['item']['name']
else:
    print ('Current playback is not a track.')
    exit()

#Get target plist
request= sp.current_user_playlists()
plist_uri = None
for plist in request['items']: #search existing playlist
    if (plist['name'] == plist_name) & (plist['owner']['id'] == user_id):
        plist_uri = plist['uri']
    break
if not plist_uri:
    print('Target playlist not found')
    exit()
request = sp.playlist_add_items(plist_uri, [track_uri])
if request:
    print(f'Succesfully added {track_name} to {plist_name}')


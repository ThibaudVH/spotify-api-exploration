import numpy as np
import pandas as pd
import sys
from pathlib import Path
import os
from pandas.core.base import DataError
sys.path.append(Path(__file__).parent.parent.absolute().as_posix())
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError 
import config
import re
import argparse
from logutil import getlogger


parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', help = 'set the name of the playlist to be created or amended', required=True)
parser.add_argument('--file', '-f', help = 'the file containing the tracks info to be added to the playlist', required=True)
args = parser.parse_args()

if not args.name:
    print('error, must provide a non-empty playlist name')
    exit()
if not args.file:
    print('error, must provide a valid file containing the tracks to be added.')
    exit()

plist_name = args.name
plist_file = args.file

logger = getlogger('plist_upload')

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

def add_tracks_to_playlist(tracks_to_add, plist_uri, sp_client):
    """
    Add tracks to a specified playlist. Uses several operation if more than 100 tracks to add. 
    Will not add tracks with the same URI if alreadcy present in the plist.
    @params:
    tracks_to_add           - Required  : list of tracks URIs
    plist_uri               - Required  : playlist URI       
    sp_client               - Required  : spotify client
    """
    result=''
    playlist_tracks = sp.playlist_tracks(playlist_id=plist_uri)
    for track in playlist_tracks['items']['tracks']:
        plist_existing_tracks_uri.append(track['uri'])
    sp_tracks_to_add_uri = np.setdiff1d(tracks_to_add, plist_existing_tracks_uri)

    if len(sp_tracks_to_add_uri) > 100:
        floor, remainder = divmod(len(sp_tracks_to_add_uri), 100)
        for i in range(floor):
            result = sp_client.playlist_add_items(playlist_id=plist_uri, items=sp_tracks_to_add_uri[i:(i+1)*100])

    else:
        result = sp_client.playlist_add_items(playlist_id = plist_uri, items=sp_tracks_to_add_uri)
    
    logger.info(f'{len(sp_tracks_to_add_uri)} tracks added to the Spotify Playlist with URI {plist_uri}')
    return result

def search_match_spotify(row):
    sp_artist = ''
    sp_track_name = ''
    sp_uri = ''
    result = sp.search(row['query'])
    if result['tracks']['total'] > 0:
        track_found = result['tracks']['items'][0]
        artist_names =[]
        for artist in track_found['artists']: 
            artist_names.append(artist['name'])
        sp_artist = ', '.join(artist_names)
        sp_track_name = track_found['name']
        sp_uri = track_found['uri']
    return [sp_uri, sp_artist, sp_track_name]

def rework_track_names(x):
    #create a set containing harmonic keys
    harmonic_keys=[]
    for i in range (1,13):
        for j in ['A', 'B']:
            harmonic_keys.append(str(i)+str(j))

    harmonic_keys.reverse()
    for k in harmonic_keys:
        x = x.replace(k, '')
    x = x.lower()
    x = re.sub('\d\d - ', '', x)
    x = x.replace('original mix', '')
    x = x.replace('remix', '')
    x = x.replace('mix', '')
    x = x.replace("'", '')
    x = x.replace('(', '')
    x = x.replace(')','')
    x = x.replace('[','')
    x = x.replace(']','')
    x = x.replace(' -','')
    if (x.find('feat') != -1):
        x = x[0:x.find('feat')]
    x = x.strip()
    return x

def rework_artist_names(x):
    x = str(x)
    x = x.lower()
    x = x.replace('feat.', '')
    x = x.replace('feat', '')
    x = x.replace('ft.', '')
    x = x.replace('&', '')
    # x = x.replace('.', ' ')
    x = x.replace(',', '')
    x = x.replace('  ', ' ')
    x = x.strip()
    return x

def get_create_playlist(plist_name, sp_client):
    """
    Search for a playlist with that name in the user's owned playlists. 
    If not found, create a private, non-collaborative playlist with that name.
    @params:
    plist_name          - Required  : list of queries for tracks to search.
    sp_client           - Required  : Spotify Client

    """
    plist_uri=''
    result = sp_client.current_user_playlists()
    for plist in result['items']: #search existing playlist
        if (plist['name'] == plist_name) & (plist['owner']['id'] == user_id):
            plist_uri = plist['uri']
            logger.info(f'Playlist {plist_name} found in Spotify existing user playlists. Playlist URI: {plist_uri}')
        break

    if not plist_uri: #create playlist
        result = sp_client.user_playlist_create(user = user_id, name = plist_name, collaborative=False, public = False)
        plist_uri = result['uri']
        logger.info(f'Playlist {plist_name} not found in user existing playlists. Playlist created. Playlist URI: {plist_uri}')
    return plist_uri

# Load the information playlist we want to upload to spotify
try:
    plist_df = pd.read_csv(plist_file)
    logger.info(f'loaded the playlist from {plist_file}')
except:
    logger.error(f'could not load the playlist info from {plist_file}')

if not {'Name', 'Artist'}.issubset(plist_df.columns):
    raise IOError(f'the file {plist_file} does not contain valid Artist and Name columns')

    
# Initiate os env. variables for spotipy auth
os.environ['SPOTIPY_CLIENT_ID'] = config.authentication['app_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config.authentication['app_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config.authentication['app_redirect_url']

#Initiate Spotipy Client
scope = "user-library-read user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative app-remote-control streaming user-read-playback-state user-modify-playback-state user-read-currently-playing"
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,show_dialog=False))
    user_id = sp.me()['id']
    logger.info(f'Succesfully logged in to Spotify as {user_id}')
except SpotifyOauthError as err:
    logger.error(err.__class__.__name__ + ':' + str(err))

# Rework some strings so that they are matched easily when querying Spotify
plist_df['simplified_name'] = plist_df['Name'].apply(rework_track_names)
plist_df['simplified_artist'] = plist_df['Artist'].apply(rework_artist_names)

#Generate the queries for each track 
plist_df['query'] = plist_df.apply(lambda row: 'track:' + str(row['simplified_name']) + ' artist:' + str(row['simplified_artist']), axis=1)
queries = list(plist_df['query'])
logger.info('Spotify queries generated from playlist file, now querying Spotify API')

#Query Spotify to match the tracks
found = plist_df.apply(search_match_spotify, axis=1, result_type='expand')
columns = ['spotify_uri', 'spotify_artist', 'spotify_track_name']
plist_df[columns] = found
not_found_df = plist_df.loc[plist_df['spotify_uri']=='']
logger.info(f'out of {len(plist_df)} tracks, {len(not_found_df)} tracks were not matched')

# Get/Create the Spotify playlist
plist_uri, plist_existing_tracks_uri = get_create_playlist(plist_name)

#add tracks to playlist
tracks_to_add_uri = plist_df.loc[plist_df['spotify_uri']!='']['spotify_uri']
result = add_tracks_to_playlist(tracks_to_add = tracks_to_add_uri, plist_uri = plist_uri, sp_client=sp)

logger.info('Playlist upload completed.')
if len(not_found_df)>0:
    logger.info('Tracks not found:')
    for track in not_found_df.itertuples():
        track_name = getattr(track, 'Name')
        track_artist = getattr(track, 'Artist')
        track_query = getattr(track, 'query')
        logger.info(f'{track_name} - {track_artist}, queried as {track_query}')

import numpy as np
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyClientCredentials 
import config
from pathlib import Path

# from utilities.logutil import getlogger
# logger = getlogger('add_currently_playing')

def like_currently_playing(verbose=False):
    path = str(Path(__file__).parent.absolute())
    # Initiate os env. variables for spotipy auth
    os.environ['SPOTIPY_CLIENT_ID'] = config.authentication['app_id']
    os.environ['SPOTIPY_CLIENT_SECRET'] = config.authentication['app_secret']
    os.environ['SPOTIPY_REDIRECT_URI'] = config.authentication['app_redirect_url']

    #Initiate Spotipy Client
    scope = "user-follow-modify user-library-read user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative app-remote-control streaming user-read-playback-state user-modify-playback-state user-read-currently-playing"
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=path+'/cache.txt'))
        user_id = sp.me()['display_name']
        if verbose:
            print(f'Succesfully logged in to Spotify as {user_id}')
    except SpotifyOauthError as err:
        print(err.__class__.__name__ + ':' + str(err))
    # Get current playback
    request = sp.current_playback()
    if not request:
        print ('No currently playing track.')
        exit()
    if (request['item']['type']=='track'):
        track_uri = request['item']['id']
        track_name = request['item']['name']
    else:
        print ('Current playback is not a track.')
        exit()
    
    sp.current_user_saved_tracks_add([track_uri])
    print(f'Succesfully added {track_name} to liked songs') 

if __name__=="__main__":
    import argparse
    PARSER = argparse.ArgumentParser(
        description="Adds the currently playing track to the playlist in Spotify"
        )
    
    PARSER.set_defaults(verbose=False)
    PARSER.add_argument('--verbose', '-v', 
                        help = 'level of output verbose', 
                        dest='verbose', 
                        action='store_true',
                        )
    ARGS = vars(PARSER.parse_args())

    like_currently_playing(verbose=ARGS['verbose'])
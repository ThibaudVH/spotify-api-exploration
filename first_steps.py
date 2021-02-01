#%%
from utilities import authentication
from utilities import search
import config


# request authentication token, 
#TODO: would be good to initiate a client object that would have the utilities as function, 
# being instantiated by a authentication/session object call.

appid = config.authentication['app_id']
secret = config.authentication['app_secret']

access_token = authentication.get_app_access_token(app_id=appid, app_secret=secret)
print(access_token)

#%%
# Search for an artist
search_result = search.artist(artist_name='Sub Focus', auth_token=access_token)
print(search_result)

for result in search_result:
    print('Name :', result['name'], '\n', 'Genres:', result['genres'])
artist_id = search_result[0]['id']
print(artist_id)

#%%
#Get artist info by ID
search_result = search.artist_by_id(artist_id=artist_id, auth_token=access_token)
print(search_result)

#%%
# Search for an album
search_result = search.album(album_name='Mosaik', artist_name='Camo & Krooked', auth_token=access_token)
for result in search_result:
    print(result['name'])
print(len(search_result))
album_id = search_result[0]['id']
print(album_id)

# %%
# Get album info by ID
search_result = search.album_by_id(album_id=album_id, auth_token=access_token)
print(search_result)

# %%
# Search for a specific track
search_result = search.track(artist_name= 'Sub Focus', track_name = 'Airplane', auth_token=access_token)
print(len(search_result))
for result in search_result:
    artist_names =[]
    for artist in result['artists']: 
        artist_names.append(artist['name'])
    artist_names = ', '.join(artist_names)
    print('Track Name :', result['name'], '\n', 'Artists:', artist_names,'length:', result['duration_ms'])
track_id = search_result[0]['id']
print(track_id)

#%%
# Get a track info by ID
search_result = search.track_by_id(track_id = track_id, auth_token=access_token)
artist_names =[]
for artist in result['artists']: 
    artist_names.append(artist['name'])
artist_names = ', '.join(artist_names)
print('Track Name :', search_result['name'], '\n', 'Artists:', artist_names,'length:', result['duration_ms'], 'Album:', search_result['album']['name'])
# %%
# Get a track audio features by ID
search_result = search.audio_features_by_track_id(track_id = track_id, auth_token=access_token)
print(search_result)

# %%
# Get Track audio analysis by ID
search_result = search.audio_analysis_by_track_id(track_id = track_id, auth_token=access_token)
print(search_result)
# %%
# Get track recommendations
search_result = search.get_track_recommendations(seed_artists=artist_id, target_tempo=174, limit=10, auth_token=access_token)
print(len(search_result))
print(len(search_result['tracks']))

# %%

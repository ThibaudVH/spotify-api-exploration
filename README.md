# spotify-api-exploration
Generic exploration of the Spotify Web API and few tools to deal with it. This is a living repository which might give birth to more specific applications.


## Playlist Creator
This script will put seed tracks present in the file data/seed_tracks.csv into a new/existing spotify playlist. 
The script will then query the Spoify Recommendations API and get the top 10 recommended songs for each seed track and add these recommendations to the playlist.

If the name of the playlist provided matches the name of an existing playlist of the user, the tracks will be added to that playlist while avoiding duplicates.
If the name of the playlist does not match any playlist from the user, a new playlist will be created.

This scipt expects a file config.py containing your Spotifdy App ID, Secret and Redirect url in order to authenticate to the Spotify API using Spotipy. 
It also expects a csv 'seed_tracks.csv' in the folder data, with song name, artist name in the rows.

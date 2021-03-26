# spotify-api-exploration
Generic exploration of the Spotify Web API and few tools to deal with it. This is a living repository which might give birth to more specific applications.
All these scipts expects a file config.py containing your Spotifdy App ID, Secret and Redirect url in order to authenticate to the Spotify API using Spotipy (you can use config.example as template and rename it as config.py) 

## seed_playlist_creator.py
This script will put seed tracks present in the file data/seed_tracks.csv into a new/existing spotify playlist (you can use the seed_tracks.example and rename it as seed_tracks.csv for the structure).
The script will then query the Spotify Recommendations API and get the top 10 recommended songs for each seed track and add these recommendations to the playlist.

If the name of the playlist provided matches the name of an existing playlist of the user, the tracks will be added to that playlist while avoiding duplicates.
If the name of the playlist does not match any playlist from the user, a new playlist will be created.

## playlist_uploader.py
This script will upload a playlist to Spotify based on a csv containing track informations (track name, track artist). you must specify the --name of the playlist and --file containing the track informtion when running the script.




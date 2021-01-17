import requests
import json
import sys
import config

def get_app_access_token(app_id, app_secret):
    """
    This returns a basic app access token. 
    This is the most limited acess to the Spotify API and does not include any user authorization nor any access to private user information
    """
    url = 'https://accounts.spotify.com/api/token'

    payload= {'grant_type':'client_credentials'}
    token_request = requests.post(url, auth=(app_id, app_secret), data=payload)
    token_request.content

    if token_request.ok: 
        token_data = json.loads(token_request.content)
        access_token = token_data['access_token']
        return access_token
    else:
        return token_request.raise_for_status()

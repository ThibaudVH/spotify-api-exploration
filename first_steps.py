#%%
import requests
from utilities import authentication
import config

appid = config.authentication['app_id']
secret = config.authentication['app_secret']

access = authentication.get_app_access_token(app_id=appid, app_secret=secret)
print(access)
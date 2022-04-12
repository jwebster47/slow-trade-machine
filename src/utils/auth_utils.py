import os
import requests
import dotenv
from datetime import datetime
from .dotenv_utils import load_dotenv_globals

dotenv_file = load_dotenv_globals()
refresh_token = os.environ['TD_AMERITRADE_REFRESH_TOKEN']
client_id = os.environ['TD_AMERITRADE_CLIENT_ID']
current_date_str = datetime.today().strftime("%Y-%m-%d")
url = 'https://api.tdameritrade.com/v1/oauth2/token'


def reset_refresh_token():
    
    request_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'access_type': 'offline',
        'client_id': client_id
    }

    response = requests.post(url, data = request_body)

    if response.status_code == 200:
        new_refresh_token = response.json()['refresh_token']
        new_access_token = response.json()['access_token']
        dotenv.set_key(dotenv_file, 'TD_AMERITRADE_REFRESH_TOKEN', new_refresh_token)
        dotenv.set_key(dotenv_file, 'TD_AMERITRADE_ACCESS_TOKEN', new_access_token)
        dotenv.set_key(dotenv_file, 'REFRESH_TOKEN_LAST_GENERATED', current_date_str)
    else:
        raise Exception(f'Invalid response code {response.status_code} from oauth refresh token request, token may have expired (90 day lifespan).')


def reset_access_token(refresh_token):
    
    # runs before every trade event
    request_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id
    }

    response = requests.post(url, request_body)

    if response.status_code == 200:
        new_access_token = response.json()['access_token']
        dotenv.set_key(dotenv_file, 'TD_AMERITRADE_ACCESS_TOKEN', new_access_token)
    else:
        raise Exception(f'Invalid response code {response.status_code} from oauth acess token request.')
        

import os
import json
import requests
import boto3
import pandas as pd
from datetime import datetime
from utils.dotenv_utils import load_dotenv_globals

dotenv_file = load_dotenv_globals()


class Requester():

    def __init__(self, ticker, period_type='day', period=1, frequency_type='minute', frequency=1, extended_hours='false'):
        self.apikey = os.environ['TD_AMERITRADE_CLIENT_ID']
        self.ticker = ticker
        self.period_type = period_type
        self.period = period
        self.frequency_type = frequency_type
        self.frequency = frequency
        self.extended_hours = extended_hours
        self.url = self.get_request_url
        self.data = self.parse_response_to_df

        #self.current_date_str = datetime.today().strftime("%Y-%m-%d")

    @property
    def get_request_url(self):
        
        # regular hours: 9:30am - 4:00pm
        # extended hours: 4:00pm - 8:00pm
        # US Eastern Time Zone

        return f'https://api.tdameritrade.com/v1/marketdata/{self.ticker}/pricehistory?apikey={self.apikey}&periodType={self.period_type}' + \
               f'&period={self.period}&frequencyType={self.frequency_type}&frequency={self.frequency}&needExtendedHoursData={self.extended_hours}'


    @property
    def parse_response_to_df(self):

        response = self.make_request()
        payload = json.loads(response.text)
        df = pd.DataFrame([i for i in payload['candles']])
        df['datetime'] = [datetime.fromtimestamp(tstamp / 1000) for tstamp in df['datetime']]

        return df


    def make_request(self):
        
        response = requests.get(self.url)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Invalid response code {response.status_code} from oauth refresh token request.')


    def save_to_csv(self, save_directory: str, filename: str):

        self.data.to_csv(save_directory + filename + '.csv')


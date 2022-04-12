from abc import abstractmethod
import os
import json
import requests
from datetime import datetime
import pandas as pd
from utils.dotenv_utils import load_dotenv_globals


_ = load_dotenv_globals()


class Requester():

    def __init__(self, ticker_list, period_type='day', period=1, frequency_type='minute',
                frequency=1, extended_hours='false', df='false'):

        self.apikey = os.environ['TD_AMERITRADE_CLIENT_ID']
        self.ticker_list = ticker_list
        self.period_type = period_type
        self.period = period
        self.frequency_type = frequency_type
        self.frequency = frequency
        self.extended_hours = extended_hours
        self.dataframe = (False if df.lower() not in ['t', 'true', 'y', 'yes', '1'] else True)
        self.data = self.save_response_data
        
    @property
    def save_response_data(self):
        
        response_data_dict = {}
        for ticker in self.ticker_list:
            url = self.get_request_url(ticker)
            response = self.make_request(url)
            response_data = self.parse_response_data(response)
            data = (response_data if not self.dataframe else self.response_as_df(response_data))
            response_data_dict[ticker] = data
        
        return response_data_dict
    
    def get_request_url(self, ticker: str):
        
        # regular hours: 9:30am - 4:00pm
        # extended hours: 4:00pm - 8:00pm
        # US Eastern Time Zone

        return f'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory?apikey={self.apikey}&periodType={self.period_type}' + \
               f'&period={self.period}&frequencyType={self.frequency_type}&frequency={self.frequency}&needExtendedHoursData={self.extended_hours}'

    @ abstractmethod
    def make_request(self, url: str):
        
        response = requests.get(url)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Invalid response code {response.status_code} from request.')

    @abstractmethod
    def parse_response_data(self, response: requests.Response):

        payload = json.loads(response.text)

        return payload['candles']

    @abstractmethod
    def response_as_df(self, response_data):

        df = pd.DataFrame([i for i in response_data])
        df['datetime'] = [datetime.fromtimestamp(tstamp / 1000) for tstamp in df['datetime']]

        return df


from abc import abstractmethod
import os
import json
import requests
from datetime import datetime
import pandas as pd
from utils.dotenv_utils import load_dotenv_globals


_ = load_dotenv_globals()


class Requester:

    def __init__(

        self,
        ticker_list: list,
        period_type='day',
        period=1,
        frequency_type='minute',
        frequency=1,
        extended_hours='false',

    ):

        self.apikey = os.environ['TD_AMERITRADE_CLIENT_ID']
        self.ticker_list = ticker_list
        self.period_type = period_type
        self.period = period
        self.frequency_type = frequency_type
        self.frequency = frequency
        self.extended_hours = extended_hours
        self.data = self.response_data
        
    @property
    def response_data(self):
        
        response_data_dict = {}
        for ticker in self.ticker_list:
            url = self.get_request_url(ticker)
            response = self.make_request(url)
            response_data = self.parse_response_data(response)
            if len(response_data) > 0:
                data = self.response_as_df(response_data)
                response_data_dict[ticker] = data
        
        return response_data_dict
    
    def get_request_url(self, ticker: str):
        
        # regular hours: 9:30am - 4:00pm
        # extended hours: 4:00pm - 8:00pm
        # US Eastern Time Zone

        return f'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory?apikey={self.apikey}&periodType={self.period_type}' + \
               f'&period={self.period}&frequencyType={self.frequency_type}&frequency={self.frequency}&needExtendedHoursData={self.extended_hours}'

    @staticmethod
    def make_request(url: str):
        
        response = requests.get(url)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Invalid response code {response.status_code} from request.')

    @staticmethod
    def parse_response_data(response: requests.Response):

        payload = json.loads(response.text)

        return payload['candles']

    @staticmethod
    def response_as_df(response_data):

        df = pd.DataFrame([i for i in response_data])
        df['datetime'] = [datetime.fromtimestamp(tstamp / 1000) for tstamp in df['datetime']]

        return df


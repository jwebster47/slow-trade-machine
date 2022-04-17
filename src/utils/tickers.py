import os
from .dotenv_utils import load_dotenv_globals

_ = load_dotenv_globals()

ticker_str = os.environ['TICKERS']

def get_tickers():
    ticker_list = [ticker.strip() for ticker in ticker_str.split(',')]
    return ticker_list

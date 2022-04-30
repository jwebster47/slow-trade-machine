from datetime import datetime
from utils import s3_utils
from requester import Requester
from utils.tickers import get_tickers

ticker_list = get_tickers()
day_of_week = datetime.today().weekday()

if __name__ == '__main__':
    if day_of_week < 5:
        rq = Requester(ticker_list)
        history = rq.data
        s3_utils.upload_dict(history, 'history')

from datetime import datetime
from utils import s3_utils
from requester import Requester
from utils.tickers import get_tickers

ticker_list = get_tickers()
day_of_week = datetime.today().weekday()

if __name__ == '__main__':
    rq = Requester(ticker_list)
    history = rq.data
    if day_of_week < 5:
        s3_utils.upload_dict(history, 'history')

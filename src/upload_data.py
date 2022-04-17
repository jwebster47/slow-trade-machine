from utils import s3_utils
from requester import Requester
from utils.tickers import get_tickers

ticker_list = get_tickers()

if __name__ == '__main__':
    rq = Requester(ticker_list)
    history = rq.data
    s3_utils.upload_dict(history, 'history')
import os
import datetime
from dateutil import parser
from utils import auth_utils
from utils.dotenv_utils import load_dotenv_globals

# TODO add logging

def reset():
    _ = load_dotenv_globals()
    current_date = datetime.datetime.today()
    last_token_generation_date = parser.parse(os.environ['REFRESH_TOKEN_LAST_GENERATED'])
    date_delta_in_days = (current_date - last_token_generation_date).days

    if date_delta_in_days > 75:
        auth_utils.reset_refresh_token()


if __name__ == '__main__':
    reset()

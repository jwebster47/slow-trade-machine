import os
from utils import auth_utils
from utils.dotenv_utils import load_dotenv_globals

def reset():
    _ = load_dotenv_globals()
    auth_utils.reset_access_token(os.environ['TD_AMERITRADE_REFRESH_TOKEN'])


if __name__ == '__main__':
    reset()
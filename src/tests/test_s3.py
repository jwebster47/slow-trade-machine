# make into a pytest test
import pandas as pd
from requester import Requester
from utils import s3_utils
from datetime import date
# from utils.path_utils import source_path
# from utils.dotenv_utils import load_dotenv_globals


# test remove folders in bucket

# test upload file to new folder

# test download file

# if __name__ == '__main__':
#     s3_utils.upload_file(source_path() + '/test_data/testfile.csv', 'equitypricehistory', 'test_data')

if __name__ == '__main__':
    df = Requester('AAPL').data
    s3_utils.upload_df_as_csv(df, 'testfile', 'test_data')
    df = pd.read_csv(f's3://equitypricehistory/test_data/testfile-{date.today().isoformat()}.csv', usecols=['open', 'high', 'low', 'close', 'volume', 'datetime'], index_col='datetime')
    pass
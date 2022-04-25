import os
import boto3
import gzip
import smart_open
import pandas as pd
from io import BytesIO
from .dotenv_utils import load_dotenv_globals

_ = load_dotenv_globals()
s3 = boto3.resource('s3')
bucket_name = os.environ['S3_BUCKET_NAME']


def upload_file(path_to_file: str, destination_directory_name: str = None):
    """
    Uploads existing file to s3 bucket.
    """

    filename = path_to_file.split('/')[-1]

    if destination_directory_name is None:
        destination_directory_name = str()
    else:
        destination_directory_name += '/'
        
    try:
        with open(path_to_file, 'rb') as data:
            s3.Bucket(bucket_name).put_object(Key=destination_directory_name + filename, Body=data)
    except Exception:
        raise

def upload_dict(history: dict, destination_directory_name: str = None):
    """
    Uploads a dictionary object.
    Use a filename with no extension and a destination directory with no slash character.
    """
    for key, df in history.items():
        append_df(df, key, destination_directory_name)

def append_df(df: pd.DataFrame, filename: str, destination_directory_name: str = None):
    """
    Adds data to existing file or creates it.
    Use a filename with no extension and a destination directory with no slash character.
    """

    if destination_directory_name is None:
        destination_directory_name = str()
    
    destination_directory_name += '/'

    try:
        df = pd.read_csv(f's3://{bucket_name}/{destination_directory_name}{filename}.csv.gz')
    except FileNotFoundError:
        try:
            buffer = BytesIO()
            with gzip.open(buffer, mode="wt") as f:
                df.to_csv(f, index=False)
            s3.Bucket(bucket_name).put_object(Key=destination_directory_name + filename + '.csv.gz', Body=buffer.getvalue())
        except:
            raise

    try:
        df.to_csv(smart_open.open(f's3://{bucket_name}/{destination_directory_name}{filename}.csv.gz', 'w'), index=False)
    except:
        raise


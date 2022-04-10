import os
import boto3
from datetime import date
from .dotenv_utils import load_dotenv_globals

_ = load_dotenv_globals()
s3 = boto3.resource('s3')
bucket_name = os.environ['S3_BUCKET_NAME']


def upload_file(path_to_file: str, destination_directory_name=None):

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


def upload_df_as_csv(df, filename, destination_directory_name=None):

    if destination_directory_name is None:
        destination_directory_name = str()

    df.to_csv(f's3://{bucket_name}/{destination_directory_name}/{filename}-{date.today().isoformat()}.csv')


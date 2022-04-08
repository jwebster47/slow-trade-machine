import boto3


s3 = boto3.resource('s3')

def upload_file(path_to_file: str, bucket_name: str, destination_directory_name=None) -> None:

    filename = path_to_file.split('/')[-1]

    if destination_directory_name is None:
        destination_directory_name = str()
    else:
        destination_directory_name += '/'
        
    try:
        with open(path_to_file, 'rb') as data:
            s3.Bucket(bucket_name).put_object(Key=destination_directory_name + filename, Body=data)
    except Exception as e:
        raise e
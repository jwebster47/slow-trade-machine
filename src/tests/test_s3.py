# make into a pytest test
from utils import s3_utils
from utils.path_utils import source_path

# test remove folders in bucket

# test upload file to new folder

# test download file

if __name__ == '__main__':
    s3_utils.upload_file(source_path() + '/data/testfile.csv', 'equitypricehistory', 'test_data')

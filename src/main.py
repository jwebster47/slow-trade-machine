from requests import make_request
from utils.s3_utils import send_json

response = make_request('FB')
send_json(response, destination_directory_name='Facebook')
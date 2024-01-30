import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import logging

load_dotenv()

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = os.environ['REGION']
BUCKET_NAME = os.environ['BUCKET_NAME']


s3 = boto3.client(
  "s3",
  REGION,
  aws_access_key_id=AWS_ACCESS_KEY,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file('indy2.gif', BUCKET_NAME, 'indy.gif')

#s3.download_file(BUCKET_NAME, 'indy.gif', 'newindy.gif')

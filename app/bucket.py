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


class Bucket:

    def __init__(
            self,
            aws_access_key=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region=REGION,
            bucket_name=BUCKET_NAME):

        self.bucket_name = bucket_name
        self.region = region
        self.client = boto3.client(
            "s3",
            region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key
        )

    def upload_file(self, image_binary, file_name, content_type='image/jpeg'):
        """Upload a file to an S3 bucket

        image_binary: Image binary file to upload
        file_name: file_name. Will correspond to object key in S3
        returns: aws_image_src: URL to image in S3
        """

        try:
            response = self.client.put_object(
                Body=image_binary,
                Bucket=self.bucket_name,
                Key=file_name,
                ContentType=content_type
            )

            aws_image_src = (f'https://{self.bucket_name}'
                             f'.s3.{self.region}.amazonaws.com/{file_name}')

        except ClientError as e:
            logging.error(e)
            return

        return aws_image_src

    def get_file(self, file_name):
        """Takes in a file name , returns response"""

        response = self.client.get_object(
            Bucket=self.bucket_name, Key=file_name)
        return response

    def delete_file(self, file_name):
        """Delete an image from an S3 bucket"""

        try:
            response = self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )

        except ClientError as e:
            logging.error(e)
            return

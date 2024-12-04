import boto3
import os

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), aws_session_token=os.getenv('AWS_SESSION_TOKEN'))

def upload_to_s3(file_name, bucket_name, object_name):
    s3.upload_file(file_name, bucket_name, object_name)
    return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

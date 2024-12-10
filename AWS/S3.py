import boto3
import os

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), aws_session_token=os.getenv('AWS_SESSION_TOKEN'))

def upload_to_s3(file_name, object_name):
    s3.upload_file(file_name, object_name)
    return os.getenv("S3_BUCKET_NAME"), object_name

def get_videos_by_folder(directory_name):
    return s3.list_objects_v2(Bucket=os.getenv("S3_BUCKET_NAME"), Prefix=f"{directory_name}/")
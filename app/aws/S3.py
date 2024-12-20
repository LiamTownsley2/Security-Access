import boto3
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_REGION")
)


def upload_to_s3(file_name, object_name):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        return None
    s3.upload_file(file_name, bucket_name, object_name)
    return bucket_name, object_name


def get_videos_by_folder(directory_name):
    response = s3.list_objects_v2(
        Bucket=os.getenv("S3_BUCKET_NAME"), Prefix=f"{directory_name}/"
    )
    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    else:
        print("No files found.")
        return []

def generate_share_url(bucket_name, object_key):
    return s3.generate_presigned_url('get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=3600)
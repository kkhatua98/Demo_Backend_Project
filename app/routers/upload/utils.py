import os 
import boto3 

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
S3_BUCKET = os.environ.get("S3_BUCKET")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def generate_presigned_url(s3_key: str):
    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params = {"Bucket": S3_BUCKET, "Key": s3_key},
        ExpiresIn = 600
    )
    return presigned_url
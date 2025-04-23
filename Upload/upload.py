from fastapi import FastAPI, UploadFile, File
import boto3
import os
from typing import Annotated
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = "your-bucket-name"


s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

@app.get("/generate-presigned-url")
def generate_presigned_url(file_name: Annotated[str, Query(...)]):
    key = f"uploads/{file_name}"
    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params = {"Bucket": S3_BUCKET, "Key": key},
        ExpiresIn = 600
    )

    return {
        "presigned_url": presigned_url,
        "key": key
    }

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    key = f"uploads/{file.filename}"

    # Generate pre-signed PUT URL (optional here, or use s3.upload_fileobj directly)
    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": S3_BUCKET, "Key": key},
        ExpiresIn=600
    )

    # Upload to S3 using `upload_fileobj`
    s3.upload_fileobj(file.file, S3_BUCKET, key)

    # Optionally, trigger OCR via Celery
    # ocr_task.delay(key)

    return {"message": "Uploaded successfully", "s3_key": key}

from fastapi import FastAPI, Depends, File, Form, HTTPException, Query, Body
import models
import psycopg2
from typing import Annotated
import datetime
from fastapi.security import OAuth2PasswordRequestForm
import utils
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from crud import user_crud


app = FastAPI()


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[str, Depends(utils.verify_token)],
):
    return current_user


@app.get("/generate-presigned-url")
def generate_presigned_url(file_name: Annotated[str, Query(...)], _ = Annotated[str, Depends(utils.verify_token)]):
    key = f"uploads/{file_name}"
    presigned_url = models.s3_client.generate_presigned_url(
        "put_object",
        Params = {"Bucket": models.S3_BUCKET, "Key": key},
        ExpiresIn = 600
    )

    return {
        "presigned_url": presigned_url,
        "key": key
    }


@app.post("/notify-upload/")
async def notify_upload(s3_path: Annotated[str, Body()]):
    ocr_task.delay(s3_path)
    return {"status": "ok"}
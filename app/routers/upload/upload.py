from fastapi import APIRouter, Query, Depends, Body
from typing import Annotated
import dependencies
import boto3 
import os
import utils
# from handlers import event_registry
import psycopg2
from crud import crud
import datetime
import schemas

def run_ocr():
    pass


router = APIRouter(prefix = "/file")

@router.get("/generate-presigned-url")
def generate_presigned_url(file_name: Annotated[str, Query(...)], _ = Annotated[str, Depends(dependencies.verify_token)]):
    s3_key = f"uploads/{file_name}"
    presigned_url = utils.generate_presigned_url(s3_key = s3_key)

    return {
        "presigned_url": presigned_url,
        "key": s3_key
    }


@router.post("/notify-upload")
def run_downstream_tasks(document: schemas.Document, conn: Annotated[psycopg2.extensions.connection, dependencies.get_db]):
    id = crud.push_new_doc(document, conn)
    run_ocr(document, id)

    return {"status": "Downstream tasks invoked"}
    
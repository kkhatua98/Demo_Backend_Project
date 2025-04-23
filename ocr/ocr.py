import uuid
import boto3
from PIL import Image
import pytesseract
import os
from typing import Annotated

DATABASE = os.environ.get("DATABASE")
DOCUMENT_TABLE = os.environ.get("DOCUMENT_TABLE")
USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
HOST = os.environ.get("POSTGRES_HOST")
PORT = 5432
DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIRECTORY")

import psycopg2
from typing import Generator
def get_db() -> Generator[psycopg2.extensions.connection, None, None]:
    try:
        connection = psycopg2.connect(
            database = DATABASE,
            user = USER,
            password = PASSWORD,
            host = HOST,
            port = PORT
        )
        # cursor = connection.cursor()
        # yield cursor
        yield connection
    finally:
        # print("Closing connection")
        connection.close()


def download_file(s3_path: str) -> str:
    # local_path = "/tmp/" + str(uuid.uuid4())
    local_path = DOWNLOAD_DIRECTORY + str(uuid.uuid4())
    s3 = boto3.client("s3")
    bucket_name, key = s3_path.split("/", 1)
    s3.download_file(bucket_name, key, local_path)
    return local_path

def extract_text(path: str) -> str:
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text 

def push_to_db(text: str) -> int:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO %s (column1, column2) VALUES (%s, %s) RETURNING id;",
        (DOCUMENT_TABLE, 'value1', text)
    )
    doc_id = cur.fetchone()[0]
    conn.commit()

    return doc_id

def delete_files(files) -> bool:
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")
    return True
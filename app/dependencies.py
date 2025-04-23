import psycopg2
from typing import Generator
import os

DATABASE = os.environ.get("DATABASE")
USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
HOST = os.environ.get("POSTGRES_HOST")
PORT = 5432

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
        connection.close()

def verify_token():
    pass
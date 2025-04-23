import psycopg2
import schemas
from core import logger
import datetime 
from core.utils import retry 

@retry(max_retries = 2)
def create_user(user: schemas.User, conn : psycopg2.extensions.connection):
    logger.logger.info(f"Pushing user {user.username} to DB")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users (id, name, email, folders, password, time_created) VALUES (%s, %s, %s, %s, %s, %s)""",
            (user.employee_id, user.username, user.email, user.folders, user._hashed_password, user._created_at)
        )
        conn.commit()
        logger.logger.info(f"Created new user: {user.username}")
    except Exception as e:
        logger.error(f"Error creating new user in db: {e}")
        conn.rollback()

@retry(max_retries = 2)
def push_new_doc(document: schemas.Document, conn: psycopg2.extensions.connection) -> int:
    logger.logger.info(f"Pushing new document to DB")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO docs (name, s3_path, owner, time_created) VALUES (%s, %s, %s, %s) returning id;""",
            (document.name, document.s3_path, document.owner, document._time_created)
        )
        generated_id = cursor.fetchone()[0]
        conn.commit()
        logger.logger.info(f"Created new document with id: {generated_id}")
        return generated_id
    except Exception as e:
        logger.error(f"Error pushing new docuement to db: {e}")
        conn.rollback()
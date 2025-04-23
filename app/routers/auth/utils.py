from pydantic import BaseModel 
import psycopg2
from core.logger import logger
import os 
from passlib.context import CryptContext
import datetime
import jwt

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

class Token(BaseModel):
    access_token: str
    token_type: str

def check_user(username: str, password: str, conn: psycopg2.extensions.connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username = %s", (username, ))
    user = cursor.fetchone()
    if not user:
        logger.warning(f"{username} not found.")
        return False 
    verification = pwd_context.verify(password, user[4])
    if not verification:
        logger.warning(f"Passwords do not match for user: {username}")
        return False
    logger.info(f"User logged in: {username}")
    return True

def create_access_token(username: str) -> str:
    token_expiry = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    encoded_jwt = jwt.encode({"sub": username, "exp": token_expiry}, key = SECRET_KEY, algorithm = ALGORITHM)
    logger.info(f"Token generated for {username}")
    return encoded_jwt
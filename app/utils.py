import psycopg2
from passlib.context import CryptContext
import tomli
import datetime 
import jwt
from datetime import timedelta, timezone
import os
# from dotenv import load_dotenv
from typing import Annotated 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt 
from jwt.exceptions import InvalidTokenError

# Load variables from .env into environment
# load_dotenv()

# SECRET_KEY = config["jwt-secret"]["SECRET_KEY"]
# ALGORITHM = config["jwt-secret"]["ALGORITHM"]
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
def check_user(username: str, password: str, conn : psycopg2.extensions.connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
    user = cursor.fetchone()
    if not user:
        print("User not found")
        return False
    verify_pwd = pwd_context.verify(password, user[4])
    if not verify_pwd:
        print("Password does not match")
        return False
    return True

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    print("Came here")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username

if __name__ == "__main__":
    with open("pyproject.toml", "rb") as f:
        config = tomli.load(f)
    connection = psycopg2.connect(
        database = config["database"]["database"],
        user = config["database"]["user"],
        password = config["database"]["password"],
        host = config["database"]["host"],
        port = config["database"]["port"]
    )
    result = check_user("babai", "babai@password", connection)
    connection.close()
    if result:
        print("User is valid")
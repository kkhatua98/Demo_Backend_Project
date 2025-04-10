import psycopg2
from passlib.context import CryptContext
import tomli
import datetime 
import jwt
from datetime import timedelta, timezone
import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

# with open("pyproject.toml", "rb") as f:
#     config = tomli.load(f)

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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
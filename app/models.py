from pydantic import BaseModel, Field, EmailStr, field_validator, PrivateAttr, model_validator
# import tomli
import datetime
from passlib.context import CryptContext 
from fastapi import Depends, Form
from typing import Annotated
import os 
from dotenv import load_dotenv
import boto3
import psycopg2

# Load variables from .env into environment
load_dotenv()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class User(BaseModel):
    employee_id: int = Form(..., gt = 100000, lt = 999999, description = "ID should be a 6 digit number starting with 3", example = ["323456"])
    username: str = Form(..., examples = ["username"])
    email: str = Form(..., pattern = r"^[\w\.-]+@abc\.com$", description = "Email should be from abc.com domain", examples = ["username@abc.com"])
    folders: list[str] | None = Form(default = ["common"], description = "List of folders, the user has access to")
    password: str = Form(..., min_length = 8, max_length = 20, description = "Password should be at least 8 characters long")
    confirm_password: str = Form(..., min_length = 8)

    _created_at: datetime.datetime = PrivateAttr(default_factory = datetime.datetime.now) 
    _hashed_password: str = PrivateAttr(default = '')


    @field_validator("employee_id")
    def validate_id(cls, value):
        if str(value)[0] != '3':
            raise ValueError("ID should start with 3")
        return value
    
    @field_validator("confirm_password")
    def validate_password(cls, value, values):
        if value != values.data["password"]:
            raise ValueError("Passwords do not match")
        return value
    
    @model_validator(mode = "after")
    def set_hashed_password(self):
        self._hashed_password = get_password_hash(self.password)
        return self
    
    def __str__(self):
        return f"User(id = {self.employee_id}, name = {self.username}, email = {self.email}, folders = {self.folders})"
    
    # def push_to_db(self, conn : Annotated[psycopg2.extensions.connection, Depends(get_db)]):
    def push_to_db(self, conn : psycopg2.extensions.connection):
        print(f"Pushing user {self.username} to DB")
        try:
            print("Fetched data")
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (id, name, email, folders, password, time_created) VALUES (%s, %s, %s, %s, %s, %s)""",
                (self.employee_id, self.username, self.email, self.folders, self._hashed_password, self._created_at)
            )
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()

from fastapi import File, Depends, HTTPException, UploadFile 
from typing import Annotated
async def file_size_checker(file: UploadFile) -> UploadFile:
    content = await file.read()
    if len(content) > 1024 * 1024:
        raise HTTPException(status_code = 413, detail = "File size exceeds 1MB")
    file.file.seek(0)
    return file
file_model = Annotated[UploadFile, Depends(file_size_checker)]

class Token(BaseModel):
    access_token: str 
    token_type: str

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



if __name__ == "__main__":
    # user = User(id = 323564, name = "ABCD", email = "abcd@abc.com")
    # print(user)
    # connection = get_db()
    # print(type(connection))
    # product = Product(name = "Book", price = 10.5)
    # print(product.name)
    # print(product._Product__MAX_PRICE)
    print(get_password_hash("password"))
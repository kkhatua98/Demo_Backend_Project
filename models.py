from pydantic import BaseModel, Field, EmailStr, field_validator
import tomli

with open("pyproject.toml", "rb") as f:
    config = tomli.load(f)

class User(BaseModel):
    id: int = Field(..., gt = 100000, lt = 999999, description = "ID should be a 6 digit number")
    name: str = Field(...)
    email: str = Field(..., pattern = r"^[\w\.-]+@abc\.com$", description = "Email should be from abc.com domain")
    folders: list[str] | None = Field(default_factory = list, description = "List of folders, the user has access to")

    @field_validator("id")
    def validate_id(cls, value):
        if str(value)[0] != '3':
            raise ValueError("ID should start with 3")
        return value
    
    def __str__(self):
        return f"User(id = {self.id}, name = {self.name}, email = {self.email}, folders = {self.folders})"
    
    def push_to_db(self):
        print(f"Pushing user {self.name} to DB")

from fastapi import File, Depends, HTTPException, UploadFile 
from typing import Annotated
async def file_size_checker(file: UploadFile) -> UploadFile:
    content = await file.read()
    if len(content) > 1024 * 1024:
        raise HTTPException(status_code = 413, detail = "File size exceeds 1MB")
    file.file.seek(0)
    return file
file_model = Annotated[UploadFile, Depends(file_size_checker)]


import psycopg2
from typing import Generator
# from psycopg2 import connection
def get_db() -> Generator[psycopg2.extensions.connection, None, None]:
    try:
        connection = psycopg2.connect(
            database = config["database"]["database"],
            user = config["database"]["user"],
            password = config["database"]["password"],
            host = config["database"]["host"],
            port = config["database"]["port"]
        )
        # cursor = connection.cursor()
        # yield cursor
        yield connection
    finally:
        # print("Closing connection")
        connection.close()


# if __name__ == "__main__":
    # user = User(id = 323564, name = "ABCD", email = "abcd@abc.com")
    # print(user)
    # connection = get_db()
    # print(type(connection))
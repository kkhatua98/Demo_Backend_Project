from pydantic import BaseModel, Field, EmailStr, field_validator

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

from fastapi import File, Depends, HTTPException 
from typing import Annotated
def file_size_checker(file: bytes = File(...)) -> bytes:
    if len(file) > 1024 * 1024:
        raise HTTPException(status_code = 413, detail = "File size exceeds 1MB")
    return file
file_model = Annotated[bytes, Depends(file_size_checker)]

import psycopg2
# from psycopg2 import connection
def get_db():
    try:
        connection = psycopg2.connect(
            database = "elog_db",
            user = "postgres",
            password = "postgres",
            host = "localhost",
            port = 5432
        )
        cursor = connection.cursor()
        # print(type(connection))
        yield cursor
    finally:
        print("Closing connection")
        connection.close()
        # db.clear()

from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/items/")
def read_items(db = Depends(get_db)):
    print(type(db))
    return {"db_status": "connection"}

# if __name__ == "__main__":
    # user = User(id = 323564, name = "ABCD", email = "abcd@abc.com")
    # print(user)
    # connection = get_db()
    # print(type(connection))
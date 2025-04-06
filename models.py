from pydantic import BaseModel, Field, EmailStr, field_validator, PrivateAttr, model_validator
# import tomlis
import datetime
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# with open("pyproject.toml", "rb") as f:
#     config = tomli.load(f)

class User(BaseModel):
    employee_id: int = Field(..., gt = 100000, lt = 999999, description = "ID should be a 6 digit number starting with 3", example = 323456)
    username: str = Field(..., examples = ["username"])
    email: str = Field(..., pattern = r"^[\w\.-]+@abc\.com$", description = "Email should be from abc.com domain", examples = ["username@abc.com"])
    # folders: list[str] | None = Field(default_factory = list, description = "List of folders, the user has access to")
    folders: list[str] | None = Field(default = ["common"], description = "List of folders, the user has access to")
    password: str = Field(..., min_length = 8, max_length = 20, description = "Password should be at least 8 characters long")
    confirm_password: str = Field(..., min_length = 8)
    # time_created: str = Field(default_factory = lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description = "Time when the user was created")
    # time_created: str = Field(default = None, description = "Time when the user was created")
    _created_at: datetime.datetime = PrivateAttr(default_factory = datetime.datetime.now) 
    _hashed_password: str = PrivateAttr(default = '')


    # def __init__(self, **data):
    #     super().__init__(**data)
    #     # self._created_at = "2025-04-02T12:00:00Z" 
    #     self._created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        self._hashed_password = f"hased_{self.password}"
    
    def __str__(self):
        return f"User(id = {self.employee_id}, name = {self.username}, email = {self.email}, folders = {self.folders})"
    
    def push_to_db(self):
        print(f"Pushing user {self.username} to DB")

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

from typing import ClassVar
class Product(BaseModel):
    name: str 
    price: float 
    __MAX_PRICE : ClassVar[float] = 1000.0


if __name__ == "__main__":
    # user = User(id = 323564, name = "ABCD", email = "abcd@abc.com")
    # print(user)
    # connection = get_db()
    # print(type(connection))
    # product = Product(name = "Book", price = 10.5)
    # print(product.name)
    # print(product._Product__MAX_PRICE)
    print(get_password_hash("password"))
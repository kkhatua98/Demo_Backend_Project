from pydantic import BaseModel, field_validator, model_validator, PrivateAttr
from fastapi import Form 
import datetime 
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

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
        self._hashed_password = pwd_context.hash(self.password)
        return self

class Document(BaseModel):
    name: str 
    s3_path: str 
    owner: str 
    
    _time_created: str = PrivateAttr(default_factory = datetime.datetime.now)
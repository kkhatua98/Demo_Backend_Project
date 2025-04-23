from typing import Annotated 
from crud import crud
import psycopg2 
from fastapi import Depends, APIRouter, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import dependencies 
import utils
from datetime import datetime
import utils
import os 
from schemas import user_schema

TOKEN_TYPE = os.environ.get("TOKEN_TYPE")

router = APIRouter(prefix = "/auth")

@router.post("/signup/")
async def create_user(user: Annotated[user_schema.User, Form()], conn : psycopg2.extensions.connection = Depends(dependencies.get_db)):
    crud.create_user(user, conn)
    return {"db_status": "User created successfully", "user": user}

@router.post("/signin/")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn: psycopg2.extensions.connection = Depends(dependencies.get_db)) -> utils.Token:
    verified = utils.check_user(form_data.username, form_data.password, conn)
    if not verified:
        raise HTTPException(status_code = 401, detail = "Invalid credentials", headers = {"WWW-Authenticate": TOKEN_TYPE})
    access_token = utils.create_access_token(username = form_data.username)
    return utils.Token(access_token = access_token, token_type = TOKEN_TYPE)
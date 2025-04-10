from fastapi import FastAPI, Depends, File, Form, HTTPException
import models
import psycopg2
from typing import Annotated
import datetime
from fastapi.security import OAuth2PasswordRequestForm
import utils
from datetime import timedelta
app = FastAPI()

@app.post("/signup/")
# async def create_user(user: Annotated[models.User, Form()]):
async def create_user(user: Annotated[models.User, Form()], conn : psycopg2.extensions.connection = Depends(models.get_db)):
    print(user._hashed_password)
    user.push_to_db(conn)
    return {"db_status": "User created successfully", "user": user}

@app.post("/signin/")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn: psycopg2.extensions.connection = Depends(models.get_db)) -> models.Token:
    verified = utils.check_user(form_data.username, form_data.password, conn)
    if not verified:
        raise HTTPException(status_code = 401, detail = "Invalid credentials", headers = {"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes = 15)
    access_token = utils.create_access_token(data = {"sub": form_data.username}, expires_delta = access_token_expires)
    return models.Token(access_token = access_token, token_type = "bearer")

import shutil
@app.post("/uploadFile/")
async def upload_file(file: models.file_model):
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    return {"file_status": "File uploaded successfully", "filename":"file.pdf"}


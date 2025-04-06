from fastapi import FastAPI, Depends, File, Form
import models
import psycopg2
from typing import Annotated
import datetime
# from passlib.context import CryptContext 

# pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

app = FastAPI()

@app.post("/signup/")
async def create_user(user: Annotated[models.User, Form()], conn : psycopg2.extensions.connection = Depends(models.get_db)):
    # print(type(db))
    # user.time_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # user._created_at = datetime.datetime.now()
    # print(user._created_at)
    try:
        print("Fetched data")
        # cursor = conn.cursor()
        # cursor.execute(
        #     """INSERT INTO users (id, name, email, folders, password, time_created) VALUES (%s, %s, %s, %s)""",
        #     (user.id, user.name, user.email, user.folders)
        # )
        # conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    return {"db_status": "User created successfully", "user": user}

import shutil
@app.post("/uploadFile/")
async def upload_file(file: models.file_model):
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    return {"file_status": "File uploaded successfully", "filename":"file.pdf"}


from fastapi import FastAPI, Depends, File
import models
import psycopg2
from typing import Annotated

app = FastAPI()

@app.post("/newUser/")
async def create_user(user: models.User, conn : psycopg2.extensions.connection = Depends(models.get_db)):
    # print(type(db))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users (id, name, email, folders) VALUES (%s, %s, %s, %s)""",
            (user.id, user.name, user.email, user.folders)
        )
        conn.commit()
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


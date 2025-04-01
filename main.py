# # from fastapi import FastAPI
# # from pydantic import BaseModel

# # class User(BaseModel):
# #     id: 

# # from typing import Annotated

# from typing import Annotated

# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse

# app = FastAPI()


# @app.post("/files/")
# async def create_files(files: Annotated[list[bytes], File()]):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfiles/")
# async def create_upload_files(files: list[UploadFile]):
#     return {"filenames": [file.filename for file in files]}


# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)


# from fastapi import FastAPI, Depends, HTTPException, Header

# app = FastAPI()

# # Dependency function to get the token from headers
# def get_current_user(abcd: str = Header(...)):
#     if abcd != "valid-token":
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     return {"user": "Alice"}

# @app.get("/secure-data/")
# def secure_data(user: dict = Depends(get_current_user)):
#     return {"message": "Secure Data", "user": user}


from fastapi import FastAPI, File, HTTPException, UploadFile, Depends
from typing import Annotated
from models import file_model
app = FastAPI()


@app.post("/upload/")
async def upload_file(file: file_model):
    return {"file_size": len(file)}

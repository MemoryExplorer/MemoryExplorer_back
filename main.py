from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import SttModule

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    result= SttModule.upload_file_asr(contents)

    return {"result": result}
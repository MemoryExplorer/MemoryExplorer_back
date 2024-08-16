from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import os
import sys

import TtsModule
import gen_question
import SttModule
import FuzzyModule
import NerModule
import SllmModule

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

# 무작위 질문 생성 엔드포인트
@app.get("/questions")
async def get_questions():

    return gen_question.gen_question()

# TTS 파일 생성 엔드포인트
@app.post("/ttsmodule")
async def gen_tts(text: str = Form(...), filename: str = Form(...)):

    return TtsModule.gen_wav_file(text, filename)

# 오디오 파일 제공 엔드포인트
@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    output_dir = 'audio_files'
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# 이미지 파일 제공 엔드포인트
@app.get("/image/{filename}")
async def get_image_file(filename: str):
    # 이미지 디렉토리 경로
    # image_dir = 'C:/MemoryExplorer/MemoryExplorer_back/test_images'
    # image_dir = 'C:/Users/user/MemoryExplorer/be/test_images'
    image_dir = 'C:\\Users\\user\\memoryexplorer\\MemoryExplorer_back\\test_images'

    file_path = os.path.join(image_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

# 녹음 된 오디오 파일 수신 및 처리 엔드포인트
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    result = SttModule.upload_file_asr(contents)
    score = FuzzyModule.fuzzy_string(result, 9)

    return {"result": result, "score": score}
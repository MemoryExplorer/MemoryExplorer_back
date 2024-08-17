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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, 'test_images')

    file_path = os.path.join(image_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

# 녹음 된 오디오 파일 수신 및 단어 인지력 처리 엔드포인트
@app.post("/Q1")
async def time_recognition(file: UploadFile, answer: str = Form(...)):
    contents = await file.read()
    result = SttModule.audio_to_text(contents)
    
    #result를 string type으로 변환
    result = next(iter(result))

    text_list = NerModule.ner_text_list(result)
    answer_list = NerModule.ner_text_list(answer)

    score_list = SllmModule.slm_text_list(text_list, answer_list)
    score = 0
    if not score_list:
        print("score_list is empty or None. Defaulting score to 0.")
    else:
        for item in score_list:
            try:
                # 각 항목을 실수형으로 변환
                score_value = float(item)
            except (ValueError, TypeError):
                # 변환할 수 없는 경우 0으로 처리
                score_value = 0
            # 점수 누적
            score += score_value

    return {
            "result": result, 
            "text_list": text_list,
            "answer_list": answer_list,
            "score_list": score_list,
            "score": score,
            }

# 녹음 된 오디오 파일 수신 및 시간 인지력 처리 엔드포인트
@app.post("/Q2")
async def time_recognition(file: UploadFile):
    contents = await file.read()
    result = SttModule.audio_to_text(contents)

    #result를 string type으로 변환
    result = next(iter(result))

    score = NerModule.ner_text(result)

    return {"result": result,
            "score": score}

# 녹음 된 오디오 파일 수신 및 사물 인지력 처리 엔드포인트
@app.post("/Q3")
async def object_recognition(file: UploadFile, answer: str = Form(...)):
    contents = await file.read()
    result = SttModule.audio_to_text(contents)

    #result를 string type으로 변환
    result = next(iter(result))
    
    score = SllmModule.slm_text(result, answer)

    return {
        "result": result, 
        "answer": answer,
        "score": score,
        }

# 녹음 된 오디오 파일 수신 및 따라하기 처리 엔드포인트
@app.post("/Q4")
async def repeat_recognition(file: UploadFile, answer: str = Form(...)):
    contents = await file.read()
    result = SttModule.audio_to_text(contents)

    #result를 string type으로 변환
    result = next(iter(result))

    score = FuzzyModule.fuzzy_string(result, answer)

    return {
        "result": result,
        "answer": answer,
        "score": score
        }

@app.post("/Q5")
async def time_recognition(file: UploadFile, answer: str = Form(...)):
    contents = await file.read()
    result = SttModule.audio_to_text(contents)
    
    #result를 string type으로 변환
    result = next(iter(result))

    text_list = NerModule.ner_text_list(result)
    answer_list = NerModule.ner_text_list(answer)

    score_list = SllmModule.slm_text_list(text_list, answer_list)
    score = 0
    if not score_list:
        print("score_list is empty or None. Defaulting score to 0.")
    else:
        for item in score_list:
            try:
                # 각 항목을 실수형으로 변환
                score_value = float(item)
            except (ValueError, TypeError):
                # 변환할 수 없는 경우 0으로 처리
                score_value = 0
            
        # 점수 누적
        score += score_value

    return {
            "result": result, 
            "text_list": text_list,
            "answer_list": answer_list,
            "score_list": score_list,
            "score": score,
            }
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os

import random
import generator
import SttModule
import FuzzyModule
import NerModule
import SllmModule

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용할 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# 순서대로 질문 조회
@app.get("/questions")
def get_questions():
    return generator.questions

# question_key 값과 일치하는 오디오파일 조회
@app.get("/audio/{question_key}")
def get_audio(question_key: str):
    audio_directory = "static/audio_files/questions"
    audio_filename = f"{question_key}.wav"
    audio_path = os.path.join(audio_directory, audio_filename)

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(audio_path)

# 랜덤 단어 3개 조회
@app.get("/random-words")
def get_random_words():
    # words 데이터에서 키를 추출
    word_keys = list(generator.words.keys())
    
    # 무작위로 3개의 단어를 선택
    selected_keys = random.sample(word_keys, min(3, len(word_keys)))
    
    # 선택된 단어들의 한글 번역을 반환
    result = {key: generator.get_word_translation(key) for key in selected_keys}
    
    return result

# word_key 값과 일치하는 오디오파일 조회
@app.get("/audio/word/{word_key}")
def get_word_audio(word_key: str):
    audio_directory = "static/audio_files/words"
    audio_filename = f"{word_key}.wav"
    audio_path = os.path.join(audio_directory, audio_filename)

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(audio_path)

# 랜덤 이미지명 1개 조회
@app.get("/random-image-word")
def get_random_image_word():
    # imgs 데이터에서 키를 추출
    image_keys = list(generator.imgs.keys())
    
    if not image_keys:
        raise HTTPException(status_code=404, detail="No images found")

    # 무작위로 하나의 이미지 선택
    selected_key = random.choice(image_keys)
    
    # 선택된 이미지의 한글 번역을 반환
    result = {selected_key: generator.imgs[selected_key]}
    
    return result

# img_key 값과 일치하는 이미지파일 조회
@app.get("/image/{img_key}")
def get_image(img_key: str):
    image_directory = "static/img_files"
    image_filename = f"{img_key}.jpg"  # 이미지 파일 확장자는 상황에 맞게 조정
    image_path = os.path.join(image_directory, image_filename)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(image_path)

# 랜덤 문장 1개 조회
@app.get("/random-sentence")
def get_random_sentence():
    # sentences 데이터에서 랜덤하게 하나의 문장을 선택
    if not generator.sentences:
        raise HTTPException(status_code=404, detail="No sentences found")

    selected_sentence = random.choice(generator.sentences)
    return selected_sentence

# sentence_key 값과 일치하는 오디오파일 조회
@app.get("/audio/sentence/{sentence_key}")
def get_sentence_audio(sentence_key: str):
    audio_directory = "static/audio_files/sentences"
    audio_filename = f"{sentence_key}.wav"
    audio_path = os.path.join(audio_directory, audio_filename)

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(audio_path)

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
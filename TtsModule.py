from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import random
from datetime import datetime

# MeloTTS 디렉토리를 Python 경로에 추가
sys.path.append(os.path.abspath('MeloTTS'))
from melo.api import TTS

# TTS 모델 설정
speed = 1.0
device = 'cpu'  # 또는 'cuda:0'
model = TTS(language='KR', device=device)

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 10가지 단어 데이터
word_list = [
    "탁자", "냄비", "접시", "모래", "라디오",
    "나무", "자동차", "버스", "가위", "모자"
]

# Q4에서 사용할 문장 데이터
sentences = [
    "간장 공장 공장장",
    "백문이 불여일견",
    "고래 싸움에 새우 등 터진다",
    "저 소나무 철갑을 두른 듯",
    "유월의 햇빛이 밝다",
    "단풍 곱게 물든 햇살",
    "삼천리 화려 강산",
    "바람 서리 불변함",
    "들판을 가르는 푸른 바람",
    "티없이 맑은 하늘"
]

# TTS 모듈 엔드포인트
@app.post("/ttsmodule")
async def tts_module(text: str = Form(...), filename: str = Form(...)):
    # 오디오 파일을 저장할 디렉토리 설정
    output_dir = 'audio_files'
    os.makedirs(output_dir, exist_ok=True)

    # 파일명이 .wav 확장자로 끝나도록 처리
    if not filename.endswith('.wav'):
        filename += '.wav'

    # 파일 경로 구성
    output_path = os.path.join(output_dir, filename)

    try:
        # TTS를 사용하여 오디오 파일 생성
        speaker_ids = model.hps.data.spk2id
        model.tts_to_file(text, speaker_ids['KR'], output_path, speed=speed)
        return {"message": f"File saved to {output_path}"}
    except Exception as e:
        return {"error": str(e)}

# 오디오 파일 제공 엔드포인트
@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    output_dir = 'audio_files'
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# 질문 데이터를 제공하는 엔드포인트
@app.get("/api/questions")
async def get_questions():
    # Q1에서 사용할 세 가지 무작위 단어 선택
    selected_words = random.sample(word_list, 3)
    random_text = ". ".join(selected_words) + "."

    # Q4에서 사용할 무작위 문장 선택
    selected_sentence = random.choice(sentences)

    # 음성 생성에 사용할 텍스트
    audio_text1 = f"지금 말하는 세 가지 단어를 잘 기억해 주세요. {random_text}"
    audio_text4 = f"지금 들리는 문장을 잘 듣고 그대로 따라해주세요. {selected_sentence}"

    # 현재 날짜와 요일 계산
    now = datetime.now()
    month = now.strftime("%m월")
    weekday = now.strftime("%A")

    # 한글 요일 변환
    weekdays_kr = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }
    weekday_kr = weekdays_kr.get(weekday, "요일")

    data = [
        {"key": "Q1", "value": "지금 말하는 세가지 단어를 잘 기억해 주세요.", "audio_text1": audio_text1},
        {"key": "Q2", "value": "오늘은 몇 월, 무슨 요일 입니까?", "month": month, "weekday": weekday_kr},
        {"key": "Q4", "value": "지금 들리는 문장을 잘 듣고 그대로 따라해주세요.", "audio_text4": audio_text4},
        {"key": "Q5", "value": "처음에 말했던 세가지 단어 중 한개만 말해주세요."},
        {"key": "Q6", "value": "처음에 말했던 세가지 단어 중 또 다른 한개를 말해주세요."},
        {"key": "Q7", "value": "처음에 말했던 세가지 단어 중 남은 한개를 말해주세요."}
    ]
    return {"questions": data, "selected_words": selected_words, "selected_sentence": selected_sentence}

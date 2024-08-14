# import sys
# import os

# # MeloTTS 디렉토리를 Python 경로에 추가
# sys.path.append(os.path.abspath('MeloTTS'))

# from melo.api import TTS

# # Speed is adjustable
# speed = 1.0
# device = 'cpu'  # or 'cuda:0'

# text = "나는 홍길동입니다."
# model = TTS(language='KR', device=device)
# speaker_ids = model.hps.data.spk2id

# output_path = 'kr.wav'
# model.tts_to_file(text, speaker_ids['KR'], output_path, speed=speed)





# # STEP 1
# from fastapi import FastAPI, Form
# import sys
# import os
# sys.path.append(os.path.abspath('MeloTTS'))
# from melo.api import TTS

# # STEP 2
# speed = 1.0
# device = 'cpu'
# model = TTS(language='KR', device=device)

# app = FastAPI()

# @app.post("/ttsmodule")
# async def login(text: str = Form()):
#     # STEP 3
#     # text = "안녕하세요! 오늘은 날씨가 정말 좋네요."

#     # STEP 4
#     speaker_ids = model.hps.data.spk2id

#     # STEP 5
#     output_path = 'kr.wav'
#     model.tts_to_file(text, speaker_ids['KR'], output_path, speed=speed)




from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import os
import sys

sys.path.append(os.path.abspath('MeloTTS'))
from melo.api import TTS

# TTS 모델 설정
speed = 1.0
device = 'cpu'
model = TTS(language='KR', device=device)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱의 주소를 명시
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ttsmodule")
async def tts_module(text: str = Form(), filename: str = Form()):
    # Ensure the directory exists
    output_dir = 'audio_files'
    os.makedirs(output_dir, exist_ok=True)

    # Ensure the filename has the .wav extension
    if not filename.endswith('.wav'):
        filename += '.wav'

    # Construct the file path
    output_path = os.path.join(output_dir, filename)

    # Generate the speech file
    speaker_ids = model.hps.data.spk2id
    model.tts_to_file(text, speaker_ids['KR'], output_path, speed=speed)

    return {"message": f"File saved to {output_path}"}

@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    output_dir = 'audio_files'
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


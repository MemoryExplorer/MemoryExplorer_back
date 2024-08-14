from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from melo.api import TTS
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱이 실행 중인 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TTS 모델 초기화
speed = 1.0
device = 'cpu'  # or 'cuda:0' (CUDA 장치가 있는 경우)
model = TTS(language='KR', device=device)
speaker_ids = model.hps.data.spk2id

# 정적 파일 경로 설정
OUTPUT_DIR = Path("output_files")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/files", StaticFiles(directory=OUTPUT_DIR), name="files")

# 요청 데이터 모델 정의
class TTSRequest(BaseModel):
    text: str
    speed: float = 1.0
    output_path: str = 'output.wav'

@app.post("/synthesize/")
async def synthesize(request: TTSRequest):
    try:
        # 파일 경로 설정
        output_file_path = OUTPUT_DIR / request.output_path
        
        # TTS 변환
        model.tts_to_file(request.text, speaker_ids['KR'], str(output_file_path), speed=request.speed)
        
        # 성공 메시지와 파일 경로 반환
        return {
            "message": "TTS synthesis complete",
            "output_path": f"/files/{request.output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 서버 실행을 위한 메인 함수
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

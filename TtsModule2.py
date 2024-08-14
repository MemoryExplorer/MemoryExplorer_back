from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from melo.api import TTS

# FastAPI 인스턴스 생성
app = FastAPI()

# TTS 모델 초기화
speed = 1.0
device = 'cpu'  # or 'cuda:0'
model = TTS(language='KR', device=device)
speaker_ids = model.hps.data.spk2id

# 요청 데이터 모델 정의
class TTSRequest(BaseModel):
    text: str
    speed: float = 1.0
    output_path: str = 'output.wav'

@app.post("/synthesize/")
async def synthesize(request: TTSRequest):
    try:
        # TTS 변환
        model.tts_to_file(request.text, speaker_ids['KR'], request.output_path, speed=request.speed)
        return {"message": "TTS synthesis complete", "output_path": request.output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 서버 실행을 위한 메인 함수
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

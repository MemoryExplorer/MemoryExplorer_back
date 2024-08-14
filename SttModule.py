from transformers import pipeline
from io import BytesIO
import soundfile as sf
import torch

# GPU 사용 여부 확인 및 설정
device = 0 if torch.cuda.is_available() else -1

# Whisper 모델을 사용한 음성 인식 파이프라인 생성
whisper_small = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=device)

def upload_file_asr(contents):
    audio_stream = None
    try:
        # 바이트 데이터를 BytesIO 객체로 변환
        audio_stream = BytesIO(contents)

        # BytesIO 객체에서 numpy 배열로 변환
        audio_data, sample_rate = sf.read(audio_stream)

        # 오디오 데이터 유효성 확인
        if audio_data.size == 0:
            raise ValueError("Empty audio data")
        
        # 스테레오를 모노로 변환
        if len(audio_data.shape) > 1 and audio_data.shape[1] == 2:
            audio_data = audio_data.mean(axis=1)
                
        # Whisper 모델에 입력할 포맷 확인
        audio_input = {"array": audio_data, "sampling_rate": sample_rate}

        # 오디오 파일을 텍스트로 변환
        result = whisper_small(audio_input, generate_kwargs={"language": "korean"})

        # 변환된 텍스트를 반환
        return {"text": result['text']}

    except Exception as e:
        # 오류 발생 시 오류 메시지 반환
        return {"error": str(e)}
    
    finally:
        if audio_stream is not None:
            # BytesIO 객체 초기화(메모리 해제)
            audio_stream.close()
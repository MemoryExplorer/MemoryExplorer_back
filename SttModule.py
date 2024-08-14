from transformers import pipeline
from io import BytesIO
import soundfile as sf
import librosa

# Whisper 모델을 사용한 음성 인식 파이프라인 생성
whisper_small = pipeline("automatic-speech-recognition", model="openai/whisper-small")

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
        
        # 오디오 데이터를 목표 샘플링 레이트로 리샘플링
        audio_data, sample_rate = resample_audio(audio_data, sample_rate, 16000)  # Whisper 모델이 16000Hz를 권장합니다.

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

def resample_audio(audio_data, orig_sr, target_sr=16000):
    if orig_sr != target_sr:
        # librosa.resample 호출 시 인자 이름을 사용
        audio_data = librosa.resample(y=audio_data, orig_sr=orig_sr, target_sr=target_sr)
    return audio_data, target_sr
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# from transformers import pipeline

sentence_list = [
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

def fuzzy_string(result, number):

    # 문자열 유사도 계산
    similarity_score = fuzz.ratio(result, sentence_list[number])

    return similarity_score

# whisper_small = pipeline("automatic-speech-recognition", model="openai/whisper-small")
# result = whisper_small("9.wav", generate_kwargs={"language": "korean"})
# print(result['text'])

# print(fuzzy_string(result['text'], 9))
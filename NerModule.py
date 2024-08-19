from transformers import pipeline
from datetime import datetime

classifier = pipeline("ner", model="KoichiYasuoka/roberta-large-korean-upos")

def ner_text(text):
    score = 0
    month = datetime.today().month
    weekday = datetime.today().weekday()

    result = classifier(text)

    for i in range(len(result)):
        print(result[i])
        if result[i]['entity'] == 'B-NOUN' or result[i]['entity'] == 'B-CONJ':
            if result[i]['word'] == str(month):
                score += 0.5
            else:
                continue
        elif result[i]['entity'] == 'NOUN':
            if weekday == 0 and result[i]['word'] == "월요일":
                score += 0.5
            elif weekday == 1 and result[i]['word'] == "화요일":
                score += 0.5
            elif weekday == 2 and result[i]['word'] == "수요일":
                score += 0.5
            elif weekday == 3 and result[i]['word'] == "목요일":
                score += 0.5
            elif weekday == 4 and result[i]['word'] == "금요일":
                score += 0.5
            elif weekday == 5 and result[i]['word'] == "토요일":
                score += 0.5
            elif weekday == 6 and result[i]['word'] == "일요일":
                score += 0.5

    return score        

def ner_text_list(text):
    result = classifier(text)

    text_list = []

    for i in range(len(result)):
        # print(result[i])
        if result[i]['entity'] == 'NOUN' or result[i]['entity'] == 'B-NOUN':
            text_list.append(result[i]['word'])

    return text_list


# stt로 local wav file 처리부터 진행할 때 사용

# import torch

# # GPU 사용 여부 확인 및 설정
# device = 0 if torch.cuda.is_available() else -1

# # Whisper 모델을 사용한 음성 인식 파이프라인 생성
# whisper_small = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=device)

# result_text = whisper_small("word_recording5.wav", generate_kwargs={"language": "korean"})
# words = result_text['text']

# print(result_text['text'])
# print(ner_text_list(words))
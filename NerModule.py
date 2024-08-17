from transformers import pipeline
from datetime import datetime

from transformers import pipeline

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
        if result[i]['entity'] == 'NOUN':
            text_list.append(result[i]['word'])

    return text_list

# whisper_small = pipeline("automatic-speech-recognition", model="openai/whisper-small")
# result_text = whisper_small("1.wav", generate_kwargs={"language": "korean"})
# print(result_text['text'])

# print(ner_text_list(result_text['text']))
# print(ner_text_list(result_text['text'])[1])
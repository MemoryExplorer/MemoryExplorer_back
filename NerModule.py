from transformers import pipeline

# text = "The Golden State Warriors are an American professional basketball team based in San Francisco."
# text = "오늘은 2024년 8월 14일, 현재 시간은 오후 1시 57분 입니다"
text = "오늘은 일요일이지"

classifier = pipeline("ner", model="KoichiYasuoka/roberta-large-korean-upos")
# classifier = pipeline("ner", model="igorsterner/xlmr-multilingual-sentence-segmentation")
result = classifier(text)

print(result)
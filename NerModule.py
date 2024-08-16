from transformers import pipeline

def ner_text(text):
    classifier = pipeline("ner", model="KoichiYasuoka/roberta-large-korean-upos")
    result = classifier(text)

    print(result)

ner_text("8월 금요일")
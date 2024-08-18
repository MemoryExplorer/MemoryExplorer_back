questions = [
    {"key": "Q1", "value": "지금 말하는\n세 가지 단어를\n잘 기억해 주세요."},
    {"key": "Q2", "value": "오늘은\n몇 월, 무슨 요일\n입니까?"},
    {"key": "Q3", "value": "사진 속 \n물체의 이름은 \n무엇인가요?"},
    {"key": "Q4", "value": "지금 들리는 \n문장을 잘 듣고 \n그대로 따라해주세요."},
    {"key": "Q5", "value": "처음에 들려주었던 \n세 가지 단어를 \n말해주세요."}
]
sentences = [
    {"key": "soy", "value": "간장 공장 공장장"},
    {"key": "seeing", "value": "백문이 불여일견"},
    {"key": "whales", "value": "고래 싸움에 새우 등 터진다"},
    {"key": "pine", "value": "저 소나무 철갑을 두른 듯"},
    {"key": "June", "value": "유월의 햇빛이 밝다"},
    {"key": "leaves", "value": "단풍 곱게 물든 햇살"},
    {"key": "land", "value": "삼천리 화려 강산"},
    {"key": "wind", "value": "바람 서리 불변함"},
    {"key": "fields", "value": "들판을 가르는 푸른 바람"},
    {"key": "sky", "value": "티없이 맑은 하늘"}
]
words = {
    "table": "탁자",
    "pot": "냄비",
    "plate": "접시",
    "sand": "모래",
    "radio": "라디오",
    "tree": "나무",
    "car": "자동차",
    "bus": "버스",
    "scissors": "가위",
    "hat": "모자"
}
imgs = {
    "airplane": "비행기",
    "apple": "사과",
    "banana": "바나나",
    "bicycle": "자전거",
    "cat": "고양이",
    "fan": "선풍기",
    "glasses": "안경",
    "hammer": "망치",
    "rubber_gloves": "고무장갑",
    "umbrella": "우산"
}

# 이 정보를 이용하여 단어의 한글 번역을 반환
def get_word_translation(word):
    return words.get(word, word)
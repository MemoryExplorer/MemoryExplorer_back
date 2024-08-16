import os
import random
from datetime import datetime

word_list = [
    "탁자", "냄비", "접시", "모래", "라디오",
    "나무", "자동차", "버스", "가위", "모자"
]

sentences = [
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

translations = {
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

# 이미지 디렉토리 경로
# image_dir = 'C:/MemoryExplorer/MemoryExplorer_back/test_images'
image_dir = 'C:/Users/user/MemoryExplorer/be/test_images'

# 질문 데이터를 제공
def get_translation(image_name):
    # 딕셔너리에서 키가 존재하면 값을 반환
    return translations.get(image_name, "번역이 없습니다")

def gen_question():
    # Q1에서 사용할 세 가지 무작위 단어 선택
    selected_words = random.sample(word_list, 3)
    random_text = ". ".join(selected_words) + "."

    # Q4에서 사용할 무작위 문장 선택
    selected_sentence = random.choice(sentences)

    # 음성 생성에 사용할 텍스트
    audio_text1 = f"지금 말하는 세 가지 단어를 잘 기억해 주세요. {random_text}"
    audio_text4 = f"지금 들리는 문장을 잘 듣고 그대로 따라해주세요. {selected_sentence}"

    # 현재 날짜와 요일 계산
    now = datetime.now()
    month = now.strftime("%m월")
    weekday = now.strftime("%A")

    # 한글 요일 변환
    weekdays_kr = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }
    weekday_kr = weekdays_kr.get(weekday, "요일")
    
    # 이미지 파일을 랜덤하게 선택
    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    selected_image = random.choice(image_files) if image_files else None
    image_name_en, _ = os.path.splitext(selected_image)
    translation = get_translation(image_name_en)

    # 질문 데이터 구성
    data = [
        {"key": "Q1", "value": "지금 말하는\n세 가지 단어를\n잘 기억해 주세요.", "audio_text": audio_text1},
        {"key": "Q2", "value": "오늘은\n몇 월, 무슨 요일\n입니까?", "month": month, "weekday": weekday_kr},
        {"key": "Q3", "value": "사진 속 \n물체의 이름은 \n무엇인가요?", "image_filename": selected_image},
        {"key": "Q4", "value": "지금 들리는 \n문장을 잘 듣고 \n그대로 따라해주세요.", "audio_text": audio_text4},
        {"key": "Q5", "value": "처음에 들려주었던 \n세 가지 단어를 \n말해주세요.", "audio_text": audio_text4}
        # {"key": "Q5", "value": "처음에 말했던 세가지 단어 중 한개만 말해주세요."},
        # {"key": "Q6", "value": "처음에 말했던 세가지 단어 중 또 다른 한개를 말해주세요."},
        # {"key": "Q7", "value": "처음에 말했던 세가지 단어 중 남은 한개를 말해주세요."}
    ]
    return {
        "questions": data,
        "selected_words": selected_words,
        "selected_sentence": selected_sentence,
        "image_name": translation
    }
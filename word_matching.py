from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

from transformers import AutoModelForCausalLM, AutoTokenizer
from difflib import SequenceMatcher

import numpy as np
from itertools import permutations

# 모델과 토크나이저 로드
device = "cuda" # the device to load the model onto

bert_tokenizer = BertTokenizer.from_pretrained('kykim/bert-kor-base')
bert_model = BertModel.from_pretrained('kykim/bert-kor-base')

llm_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-0.5B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
llm_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

def get_embedding(text):
    """입력된 텍스트의 BERT 임베딩을 반환합니다."""
    inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # [CLS] 토큰의 임베딩을 사용합니다.
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# slm을 이용한 두 단어의 비교
def llm_judge(text1, text2):
    prompt = f"{text1}, {text2}:"
    messages = [
        {"role": "system", "content": "당신은 주어진 두 단어의 의미를 비교하는 단어 분석가입니다."},
        {"role": "system", "content": "결과는 반드시 '유사함' 또는'유사하지 않음'이어야 합니다."},
        {"role": "user", "content": prompt}
    ]

    text = llm_tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = llm_tokenizer([text], return_tensors="pt").to(device)

    generated_ids = llm_model.generate(
        model_inputs.input_ids,
        max_new_tokens=520
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = llm_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    result = "그러나" in response or "유사함" not in response
    print(f"result: {result}")

    return result

def slm_text(text, answer):
    # 단순 단어(형태) 비교
    matcher_score = SequenceMatcher(None, text, answer).ratio()
    print(f"matcher_score: {matcher_score}")

    if matcher_score == 1.0:
        return matcher_score
    else:
        #KoBert를 통한 두 단어의 유사도 점수 계산
        """두 텍스트 간의 유사도 점수를 계산합니다."""
        text1 = get_embedding(text)
        text2 = get_embedding(answer)
        # 코사인 유사도 계산
        similarity = cosine_similarity([text1], [text2])[0][0]
        print(f"similarity: {similarity}")

        # slm을 통한 두 단어 비교
        result = llm_judge(text, answer)

        # slm이 두 단어가 유사하지 않다고 판단하면 형태와 KoBert 유사도 평균 사용
        # 두 단어가 유사하다고 평가하면 KoBert 유사도 사용
        if result:
            score = (similarity + matcher_score) / 2
        else:
            score = similarity

        return score

def slm_text_list(text_list, answer_list):
    
    n = len(text_list)
    m = len(answer_list)

    if m >= n:
        matrix = np.zeros((n, m))
        
        for i in range(n):
            for j in range(m):
                matrix[i][j] = slm_text(text_list[i], answer_list[j])
        
        best_score = -1
        best_permutation = None

        # matrix에서 서로 다른 index로 최대 값 계산
        for perm in permutations(range(m), n):
            score = sum(matrix[i, perm[i]] for i in range(n))
            if score > best_score:
                best_score = score
                best_permutation = perm
    else:   # n (text_list) > m (answer_list)
        matrix = np.zeros((m, n))
        
        for i in range(m):
            for j in range(n):
                matrix[i][j] = slm_text(answer_list[i], text_list[j])
        
        best_score = -1
        best_permutation = None

        for perm in permutations(range(n), m):
            score = sum(matrix[i, perm[i]] for i in range(m))
            if score > best_score:
                best_score = score
                best_permutation = perm
        
    print(matrix)
    print(best_permutation)

    return best_score

# print(slm_text_list(['냄비', '접시', '닭', '자'], ['탁자', '냄비', '접시']))
# print(slm_text_list(['닭', '접시', '냄비'], ['탁자', '냄비', '접시']))
# print(slm_text_list(['냄비', '자'], ['탁자', '냄비', '접시']))
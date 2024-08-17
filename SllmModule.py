from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda" # the device to load the model onto
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-0.5B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

word_list = [
    "탁자", "냄비", "접시", "모래", "라디오",
    "나무", "자동차", "버스", "가위", "모자"
]

translations = [
    "비행기",
    "사과",
    "바나나",
    "자전거",
    "고양이",
    "선풍기",
    "안경",
    "망치",
    "고무장갑",
    "우산"
]

def slm_text(text, answer):

    prompt = "{0}, {1}".format(text, answer)
    messages = [
        {"role": "system", "content": """
         #Role
         - 당신은 매우 정확한 언어 분석가입니다. 
         
         #Task
         - 주어진 단어들의 의미적 유사성을 분석하고 평가해주세요. 
         - 유사성은 0부터 1 사이의 수치로 표시해주세요. 
         
         #Example
         - 소 & 소나무 : 0.0
         - 소 & 송아지 : 0.7
         - 강아지 & 송아지 : 0.3
         - 연필 & 샤프 : 0.6
         - 연필 & 볼펜 : 0.4

         #Output format
         0~1

         #Policy
         - Output format 외에는 어떠한 불필요한 내용도 응답하지 마시오.
        """},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response

def slm_text_list(text_list, answer_list):
    score_list = []
    for i in range(len(answer_list)):
        prompt = "{0}, {1}".format(text_list[i], answer_list[i])
        messages = [
            {"role": "system", "content": """
            #Role
            - 당신은 매우 정확한 언어 분석가입니다. 
            
            #Task
            - 주어진 단어들의 의미적 유사성을 분석하고 평가해주세요. 
            - 유사성은 0부터 1 사이의 수치로 표시해주세요. 
            
            #Example
            - 소 & 소나무 : 0.0
            - 소 & 송아지 : 0.7
            - 강아지 & 송아지 : 0.3
            - 연필 & 샤프 : 0.6
            - 연필 & 볼펜 : 0.4
             - 접시 & 접시 : 1.0

            #Output format
            0~1

            #Policy
            - Output format 외에는 어떠한 불필요한 내용도 응답하지 마시오.
            """},
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(device)

        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
        score_list.append(response)
    
    return score_list

# print(slm_text_list(['각자', '가위', '접시'], ['탁자', '가위', '접시']))
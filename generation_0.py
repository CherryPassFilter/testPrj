import os
import openai
from dotenv import load_dotenv

load_dotenv()

prompt = input("지시 사항을 입력하세요:  ")
openai.api_key = os.getenv("OPENAI_API_KEY")

# 초기 메시지 설정
SYSTEM_MSG = "너는 한국인 27살 약사로 행동해. 사용자의 질문에 그에 따라 답해."
messages = [
    {"role": "system", "content": SYSTEM_MSG},
    {"role": "user", "content": prompt}  # 사용자의 메시지 추가
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0,
    max_tokens=256,
)

# 출력
for choice in response.choices:
    print(choice.message['content'])


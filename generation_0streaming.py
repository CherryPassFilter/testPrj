import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Set initial message
SYSTEM_MSG = "You're a 27-year-old Korean pharmacist. When you respond to a customer, you use the Korean word ."
messages = [{"role": "system", "content": SYSTEM_MSG}]

def chat_with_gpt3():
    prompt = input("질문을 입력하세요(또는 종료하려면 '종료'를 입력하세요): ")
    
    if prompt.lower() == '종료':
        print("잘가요!")
        return
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=256,
    )

    for choice in response.choices:
        print(choice.message['content'])
        messages.append({"role": "assistant", "content": choice.message['content']})

    chat_with_gpt3()


chat_with_gpt3()
import os
from typing import Dict
#서드 파티 라이브러리
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from pydantic import BaseModel ## 파이썬 타입 주석을 사용한 데이터 유효성 검사 및 설정 관리

# 현재 스크립트의 위치를 구한다.
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

# Pydantic을 사용하여 데이터 모델을 정의,데이터 유효성 검사 
class UserRequest(BaseModel):
    user_message: str

# 제공된 파일 경로에서 템플릿 파일을 읽는 함수
def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()
    return prompt_template

# 사용자 메시지를 기반으로 응답을 생성
def generate_response(user_message: str) -> Dict[str, str]:
    qna_llm = ChatOpenAI(temperature=0.1, max_tokens=500, model="gpt-3.5-turbo")
    qna_prompt_template = ChatPromptTemplate.from_template(
        template=read_prompt_template(os.path.join(CUR_DIR, "prompt_template.txt"))
    )
    qna_chain = LLMChain(llm=qna_llm, prompt=qna_prompt_template, output_key="output")

    result = qna_chain({"user_message": user_message})

    return {"answer": result["output"]}

# 스크립트의 주 실행 부분
if __name__ == "__main__":
    while True:
        user_input = input("당신의 질문을 입력해주세요: ")
        response = generate_response(user_input)
        print("답변:", response["answer"])

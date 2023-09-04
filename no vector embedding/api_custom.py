import os
from typing import Dict

from custom_chains import (
    question_chain,
    advice_chain,
    hello_chain,
    thanks_chain,
    parse_intent_chain,
    analyze_chain,
    read_prompt_template,
    default_chain,
)
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class UserRequest(BaseModel):
    user_message: str


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
INTENT_LIST_TXT = os.path.join(CUR_DIR, "prompt_templates", "intent_list.txt")

def generate_answer(req: UserRequest) -> Dict[str, str]:
    context = req.dict()
    context["input"] = context["user_message"]
    context["intent_list"] = read_prompt_template(INTENT_LIST_TXT)

    #intent = parse_intent_chain(context)["intent"]
    intent = parse_intent_chain.run(context)

    if intent == "advice":
        answer=advice_chain.run(context)        
    elif intent == "question":
        answer = question_chain.run(context)
    elif intent == "thanks":
        answer = thanks_chain.run(context)
    elif intent == "hello":
       answer = hello_chain.run(context)
    else:
        answer = default_chain.run({"input": context["input"]})
    print("답변:", answer)

def generate_answer_from_input():
    user_message = input("질문을 입력해주세요: ") 
    req = UserRequest(user_message=user_message)
    generate_answer(req)


if __name__ == "__main__":
    while True:
        generate_answer_from_input()
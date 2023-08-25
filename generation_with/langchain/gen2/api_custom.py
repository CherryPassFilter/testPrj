import os
from typing import Dict

from custom_chains import (
    bug_step1_chain,
    bug_step2_chain,
    default_chain,
    enhance_step1_chain,
    parse_intent_chain,
    read_prompt_template,
)
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class UserRequest(BaseModel):
    user_message: str


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
INTENT_LIST_TXT = os.path.join(CUR_DIR, "prompt_templates", "intent_list.txt")

def generate_answer_from_input():
    user_message = input("질문을 입력해주세요: ")
    context = {"user_message": user_message}
    context["input"] = context["user_message"]
    context["intent_list"] = read_prompt_template(INTENT_LIST_TXT)

    intent = parse_intent_chain.run(context)

    if intent == "bug":
        answer = ""
        for step in [bug_step1_chain, bug_step2_chain]:
            answer += step.run(context)
            answer += "\n\n"  # chain1,2 더하기
    elif intent == "enhancement":
        answer = enhance_step1_chain.run(context)
    else:
        answer = default_chain.run(context)

    print("답변:", answer)

if __name__ == "__main__":
    while True:
        generate_answer_from_input()

import os
from typing import Dict

from chains import (
    drug_step1_chain,
    drug_step2_chain,
    enhance_step1_chain,
    parse_intent_chain,
    read_prompt_template,
    default_chain,
)
from database import query_db
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class UserRequest(BaseModel):
    user_message: str


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
INTENT_LIST_TXT = os.path.join(CUR_DIR, "prompt_templates", "intent_list.txt")

def gernerate_answer(req: UserRequest) -> Dict[str, str]:
    context = req.dict()
    context["input"] = context["user_message"]
    context["intent_list"] = read_prompt_template(INTENT_LIST_TXT)

    # intent = parse_intent_chain(context)["intent"]
    intent = parse_intent_chain.run(context)

    if intent == "drug":
        context["related_documents"]=query_db(context["user_message"])


        answer = ""
        for step in [drug_step1_chain, drug_step2_chain]:
            context=step(context)
            answer += context(step.output_key)
            answer += "\n\n"  # chain1,2 더하기
    elif intent == "enhancement":
        answer = enhance_step1_chain.run(context)
    else:
        answer = default_chain.run(context["user_message"])

    print("답변:", answer)

def generate_answer_from_input():
    user_message = input("질문을 입력해주세요: ")
    req = UserRequest(user_message=user_message)
    gernerate_answer(req)


if __name__ == "__main__":
    while True:
        generate_answer_from_input()

import os

from dotenv import load_dotenv
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

load_dotenv()


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYZE_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "thanks.txt"
)
ADVICE_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "advice.txt"
)

QUESTION_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "question.txt"
)
HELLO_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "hello.txt"
)
THANKS_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "thanks.txt"
)
INTENT_PROMPT_TEMPLATE = os.path.join(CUR_DIR, "prompt_templates", "parse_intent.txt")


# 제공된 파일 경로에서 템플릿 파일을 읽는 함수
def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()

    return prompt_template


def create_chain(llm, template_path, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            template=read_prompt_template(template_path)
        ),
        output_key=output_key,
        verbose=True,
    )


llm = ChatOpenAI(temperature=0.1, max_tokens=200, model="gpt-3.5-turbo")

analyze_chain = create_chain(
    llm=llm,
    template_path=ANALYZE_PROMPT_TEMPLATE,
    output_key="thanks",
)
advice_chain = create_chain(
    llm=llm,
    template_path=ADVICE_PROMPT_TEMPLATE,
    output_key="advice",
)
question_chain = create_chain(
    llm=llm,
    template_path=QUESTION_PROMPT_TEMPLATE,
    output_key="question",
)

thanks_chain = create_chain(
    llm=llm,
    template_path=THANKS_PROMPT_TEMPLATE,
    output_key="thanks",
)

hello_chain = create_chain(
    llm=llm,
    template_path=HELLO_PROMPT_TEMPLATE,
    output_key="hello",
)


parse_intent_chain = create_chain(
    llm=llm,
    template_path=INTENT_PROMPT_TEMPLATE,
    output_key="intent",
)
default_chain = ConversationChain(llm=llm, output_key="text")

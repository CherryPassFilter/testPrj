from dotenv import load_dotenv
from langchain.chains import LLMChain, SequentialChain, LLMRouterChain,ConversationChain
from langchain.chains.router import MultiPromptChain 
from langchain.chains.router.llm_router import RouterOutputParser#라우터체인파서랑 같이 사용
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from pydantic import BaseModel ## 파이썬 타입 주석을 사용한 데이터 유효성 검사 및 설정 관리
from langchain.prompts import PromptTemplate
import os


load_dotenv()
#prompt 들 불러와야 하니까
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BUG_STEP1_PROMPT_TEMPLATE = os.path.join(CUR_DIR,"prompt_templates", "bug_say_sorry.txt")
BUG_STEP2_PROMPT_TEMPLATE = os.path.join(CUR_DIR,"prompt_templates", "bug_request_context.txt")
ENHANCE_STEP1_PROMPT_TEMPLATE = os.path.join(CUR_DIR,"prompt_templates", "bug_say_sorry.txt")  
ENHANCE_STEP2_PROMPT_TEMPLATE = os.path.join(CUR_DIR,"prompt_templates", "bug_say_sorry.txt")


# 제공된 파일 경로에서 템플릿 파일을 읽는 함수
def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()
    return prompt_template

def create_chain(llm, template_path,output_key):

    return LLMChain(
    llm=llm
    prompt=ChatPromptTemplate.from_template(
         template=read_prompt_template(template_path)
    ),
   output_key=output_key,
   verbose=True,    
    )


llm=ChatOpenAI(temperature=0.1, max_tokens=200, model="gpt-3.5-turbo")

bug_step1_chain=create_chain(
    llm=llm,
    template_path=BUG_STEP1_PROMPT_TEMPLATE,
    output_key="text",
    
)

bug_step2_chain=create_chain(
    llm=llm,
    template_path=BUG_STEP2_PROMPT_TEMPLATE,
    output_key="text",
    
)

enhance_step1_chain=create_chain(
    llm=llm,
    template_path=ENHANCE_STEP1_PROMPT_TEMPLATE,
    output_key="text",
)

"""bug_sequential_chain = SequentialChain(
chain=[bug_step1_chain, bug_step2_chain]
    verbose=True,
)

enhance_sequential_chain = SequentialChain(
    chain=[enhance_step1_chain],
    verbose=True,
)
"""

#어떠한 체인으로 갈지를 구분해주는 라우터 체인으로 구별해준다.

destinations={
    "bug: Related to a bug, vulnerability, unexpected error with an existing feature",
    "documentation: Changes to documentation and examples, like .md, .rst, .ipynb files. Changes to the docs/ folder",
    "enhancement: A large net-new component, integration, or chain. Use sparingly. The largest features",
    "improvement: Medium size change to existing code to handle new use-cases",
    "nit: Small modifications/deletions, fixes, deps or improvements to existing code or docs",
    "question: A specific question about the codebase, product, project, or how to use a feature",
    "refactor: A large refactor of a feature(s) or restructuring of many files",
}
destination="\n".join(destinations)#목적지 정의
router_prompt_template=MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations)
router_prompt=PromptTemplate.from_template(
    template=router_prompt_template, output_parser=RouterOutputParser()
)

router_chain= LLMRouterChain.from_llm(llm=llm, prompt=router_prompt, verbose=True)

#모든 체인을 연결,multiprompt chain 에는 sequential chain이 들어오면 안된다.
multi_prompt_chain=MultiPromptChain{
    "bug":bug_step1_chain,
    "enhancement":enhance_step1_chain,
},
default_chain=ConversationChain(llm=llm, output_key="text"),
)

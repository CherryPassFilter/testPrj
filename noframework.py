import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_prompt_template(file_path: str)->str:
    with open(file_path,"r")as f:
        prompt_template=f.read()

        return prompt_template

def request_gpt_api(
        prompt: str, 
        model: str="gpt-3.5-turbo",
        max_tokens: int=1000, 
        temperature:float=0.8,
)->str:   
    response=openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user","content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content

SYSTEM_MSG = "You're a 27-year-old Korean pharmacist. When you respond to a customer, you use the Korean word ."

if __name__=="__main__":
    prompt_template=read_prompt_template("prompt.txt")
    
    print(request_gpt_api(prompt_template))
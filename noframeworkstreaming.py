import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()
        return prompt_template

def request_gpt_api(
        prompt: str, 
        model: str="ft:gpt-3.5-turbo-0613:personal::7r35JR4C",
        max_tokens: int=1000, 
        temperature: float=0,
) -> str:   
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    prompt_template = read_prompt_template("prompt.txt")

    while True:
        user_input = input("사용자: ")
        
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        
        prompt = prompt_template + " " + user_input
        response = request_gpt_api(prompt)
        print(f"약사: {response}")

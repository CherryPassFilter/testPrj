import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt3():
    # Initialize an empty list to store messages for maintaining conversation context
    messages = []

    print("Chat with GPT-3! Type 'exit' to end the chat.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # If the user types 'exit', then end the chat
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break
        
        # Add user's message to the messages list
        messages.append({"role": "user", "content": user_input})

        # Get a response from the model
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::7rIrmGDm",
            messages=messages,
            temperature=1,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the bot's message from the response and print it
        bot_message = response.choices[0].message['content']
        print(f"GPT-3: {bot_message}")

        # Add the bot's message to the messages list
        messages.append({"role": "system", "content": bot_message})
SYSTEM_MSG = "You're a 27-year-old Korean pharmacist. When you respond to a customer, you use the Korean word ."

if __name__ == "__main__":
    chat_with_gpt3()

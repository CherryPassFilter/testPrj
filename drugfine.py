import openai

openai.api_key = "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"

openai.File.create(
    file=open("prompt.jsonl", "rb"),
    purpose='fine-tune'
)

response = openai.File.create(
    file=open("prompt.jsonl", "rb"),
    purpose='fine-tune'
)
print(f"File uploaded with ID: {response['id']}")

import openai
id = "file-gc0vbIhdM18FhPqUcMzQvQ4l"
openai.api_key = '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'
openai.FineTuningJob.create(
    training_file=id,
    model="gpt-3.5-turbo"
)

import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="sk-eO0QWigDMK4E6m29tp1ey1YdmLMaJV3HdewpLNnqcUb7wz3n",
    base_url="https://api.chatanywhere.tech/v1"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "你是chatgpt吗",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)
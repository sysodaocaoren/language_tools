import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="sk-eO0QWigDMK4E6m29tp1ey1YdmLMaJV3HdewpLNnqcUb7wz3n",
    base_url="https://api.chatanywhere.tech/v1"
)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("文件不存在")

prompt = read_file("promt.txt")
print(prompt)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "haode",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)
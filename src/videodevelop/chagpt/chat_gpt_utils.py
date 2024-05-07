import os
from openai import OpenAI

url = "https://api.chatanywhere.tech/v1"
api_key = 'sk-eO0QWigDMK4E6m29tp1ey1YdmLMaJV3HdewpLNnqcUb7wz3n'

# api_key = "sk-FO5AXPDMYJl0uboZ504fF049B4044c35B50cFd067a44896d"
# url = "https://free.gpt.ge/v1"

def question(content):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
        base_url=url
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(str(chat_completion))
    return chat_completion.choices[0].message.content


if __name__ == '__main__':
    print(question("鲁迅和周树人的关系"))
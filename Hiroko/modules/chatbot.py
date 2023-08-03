
from pyrogram import Client

with open("Hiroko/Helper/Api.txt", "r") as fileopen:
        API = fileopen.read()


"""
fileopen = open("\Hiroko\Helper\Api.txt","r")
API = fileopen.read()
fileopen.close()
"""

import openai
from dotenv import load_dotenv

openai.api_key = API
load_dotenv()
completion = openai.Completion()


def ReplyBrain(question, chat_log=None):
    with open("Hiroko\data.txt", "r") as fileopen:  # Add the file path for chat log
    chat_log_template = fileopen.read()
    fileopen.close()

    if chat_log is None:
        chat_log = chat_log_template
    prompt = f"{chat_log}\nYou: {question}\nJarvis:"
    response = completion.create(
        model="text-davinci-882",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    chat_log_template_update = chat_log_template + f"\nYou: {question}\nJarvis: {answer}"
    with open("Hiroko\data.txt", "w") as fileopen:  # Add the file path for chat log
    fileopen.write(chat_log_template_update)
    fileopen.close()
    return answer






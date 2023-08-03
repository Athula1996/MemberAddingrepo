from pyrogram import Client, filters
from Hiroko import Hiroko

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
    with open("Hiroko/data.txt", "r") as fileopen:
        chat_log_template = fileopen.read()
        
    if chat_log is None:
        chat_log = chat_log_template
    prompt = f"{chat_log}\nYou: {question}\nJarvis:"
    response = completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=50,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    chat_log_template_update = chat_log_template + f"\nYou: {question}\nJarvis: {answer}"
    with open("Hiroko/data.txt", "w") as fileopen:
        fileopen.write(chat_log_template_update)
    return answer



@Hiroko.on_message(filters.private)
async def reply_to_message(client : Hiroko, message):
    user_id = message.from_user.id
    question = message.text
    
    # Call ReplyBrain function to get the answer
    answer = ReplyBrain(question)
    
    # Send the answer back to the user
    await client.send_message(user_id, answer)




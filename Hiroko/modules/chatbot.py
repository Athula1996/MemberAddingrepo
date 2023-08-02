import openai
from dotenv import load_dotenv

fileopen = open("Hiroko\Helper\database\api.text","r")
API = fileopen.read()
fileopen.close()

openai.api_key = API
load_dotenv()
completion = openai.Completion()

def ReplyBrain(question, chat_log=None):
    FileLog = open("", "r")
    chat_log_template = FileLog.read()
    FileLog.close()

    if chat_log is None:
        chat_log = chat_log_template

    prompt = f"{chat_log}You: {question}\nHiroko:"
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
    chat_log_template_update = chat_log_template + f"\nYou: {question}\nHiroko: {answer}"
    FileLog = open("", "w")
    FileLog.write(chat_log_template_update)
    FileLog.close()
    return answer





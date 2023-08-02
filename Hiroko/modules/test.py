
import openai
from dotenv import load_dotenv

openai.api_key = "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"
load_dotenv()
completion = openai.Completion()

def ReplyBrain(question, chat_log=None):
    if chat_log is None:
        chat_log = ""

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
    chat_log_template_update = chat_log + f"\nYou: {question}\nHiroko: {answer}"
    
    # Save the chat log to a file
    with open("Data\\chat_log.txt", "w") as FileLog:
        FileLog.write(chat_log_template_update)
    
    return answer



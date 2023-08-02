import openai
from Hiroko import Hiroko
from pyrogram import Client
from pyrogram.raw.functions.channels import GetFullChannel, GetMessages


API_KEY = "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"

CHANNEL_ID = -1001915298220  




@Hiroko.on_message()
def reply_brain(client, message):
    if message.text:
        question = message.text
        
        # Get previous chat log from the channel
        chat_log = get_chat_log(client)

        answer = generate_response(question, chat_log)
        update_chat_log(chat_log, question, answer)

        message.reply_text(answer)


def get_chat_log(client):
    # Get channel full info to access the channel chat log
    channel_info = client.send(GetFullChannel(channel=CHANNEL_ID))
    chat_log_message_id = channel_info.full_chat.about.id

    messages = client.send(GetMessages(channel=CHANNEL_ID, id=[chat_log_message_id]))

    if messages.messages:
        message = messages.messages[0]
        if getattr(message, "message", None):
            return message.message

    return ""


def generate_response(question, chat_log):
    # Use the ChatGPT API to generate a response
    import openai
    openai.api_key = API_KEY
    completion = openai.Completion()

    prompt = f"{chat_log}\nYou: {question}\nHiroko:"
    response = completion.create(
        model="text-davinci-014",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()

    return answer


def update_chat_log(chat_log, question, answer):
    chat_log_template_update = f"{chat_log}\nYou: {question}\nHiroko: {answer}"
    
    # Update the chat log in the channel
    app.send_message(CHANNEL_ID, chat_log_template_update)





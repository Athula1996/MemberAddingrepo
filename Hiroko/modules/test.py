from pyrogram import filters
from Hiroko import Hiroko

CHANNEL_ID = -1001234567890  # Replace with your channel ID


@app.on_message()
def reply_brain(client, message):
    if message.text:
        question = message.text
        chat_log = ""
        
        # Get previous chat log from the channel
        chat_log_messages = client.get_chat_history(CHANNEL_ID, limit=1).messages
        if chat_log_messages:
            chat_log = chat_log_messages[0].text
        
        prompt = f"{chat_log}\nYou: {question}\nHiroko:"
        
        # Send the prompt to the channel and get response
        response = client.send_message(CHANNEL_ID, prompt)
        
        if response:
            answer = response.text
            chat_log_template_update = f"{chat_log}\nYou: {question}\nHiroko: {answer}"
            
            # Update the chat log in the channel
            client.edit_message_text(CHANNEL_ID, response.chat.id, response.message_id, chat_log_template_update)
            
            message.reply_text(answer)
        else:
            message.reply_text("Sorry, I couldn't get a response right now. Please try again later.")


            

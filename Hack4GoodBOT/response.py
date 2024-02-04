from Hack4GoodBOT.config import config
from telegram import Update
from telegram.ext import (ContextTypes)


# Response
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ID: {update.message.from_user.id} ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if config.BOT_USERNAME in text:
            new_text: str = text.replace(config.BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I am good!'

    return 'I do not understand you...'

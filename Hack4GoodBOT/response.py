from config import config
from command import enroll_command
from telegram import Update
from telegram.ext import (ContextTypes)


# Define a function to check the current conversation state
def is_in_excluded_state(context):
    excluded_states = [enroll_command.NAME, enroll_command.AGE, enroll_command.GENDER,
                       enroll_command.WORK_STATUS, enroll_command.IMMIGRATION_STATUS,
                       enroll_command.INTERESTS, enroll_command.SKILLS, enroll_command.SUMMARY]
    return context.user_data.get('state') in excluded_states


# Response
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the bot is in an excluded state
    if is_in_excluded_state(context):
        return

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

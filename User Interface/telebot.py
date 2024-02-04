import logging
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialization
TOKEN: Final = "6915448696:AAGa692f2FuuPsMzjhyw5b-Lllnc00g5f3M"
BOT_USERNAME: Final = "@Hack4GoodBOT"

# Google Sheets information
SHEET_ID: Final = "1dQOfj3kamyPNE5X0mO7YVlKtCP4awO_XX7B4Vhf9sZc"
volunteers_sheet_name = 'Volunteers'
opportunities_sheet_name = 'Opportunities'
response_sheet_name = 'Response'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load credentials for Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)


# Response
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
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


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi there, I am Hack4GoodBOT! Type /help to see available commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/enroll - Enroll as a new volunteer\n"
        "/browse - Browse volunteering opportunities\n"
        "/attended - Check attended opportunities\n"
        "/upcoming - Check upcoming opportunities\n"
        "/feedback - Submit feedback/blog/reflection\n"
        "/certificate - Request a certificate for attended events"
    )


'''
def enroll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implement the logic to enroll as a new volunteer and save information to Google Sheets
    # ...
'''


async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Access the sheet with volunteering opportunities
    sheet = client.open_by_key(SHEET_ID).worksheet(opportunities_sheet_name)

    # Fetch all records from the sheet
    opportunities = sheet.get_all_records()

    # Check if there are any opportunities listed
    if not opportunities:
        await update.message.reply_text("Currently, there are no volunteering opportunities available.")
        return

    # Construct a message listing all opportunities
    message = "Here are the current volunteering opportunities available to join:\n\n"
    for idx, opportunity in enumerate(opportunities, start=1):
        # Strip white spaces from each piece of text to avoid unexpected indentation
        message += (f"{idx}. Event: {opportunity['Event'].strip()}\n"
                    f"Date: {opportunity['Date'].strip()}\n"
                    f"Location: {opportunity['Location'].strip()}\n"
                    f"Time: {opportunity['Time'].strip()}\n"
                    f"Duration: {opportunity['Duration'].strip()}\n"
                    f"Participants Needed: {str(opportunity['Participants Needed']).strip()}\n"
                    f"Lunch Provided?: {opportunity['Lunch Provided?'].strip()}\n"
                    f"Description: {opportunity['Description'].strip()}\n\n")

    # Send the constructed message
    await update.message.reply_text(message)


'''
def attended(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implement the logic to check attended opportunities
    # ...

def upcoming(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implement the logic to check upcoming opportunities
    # ...

def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implement the logic to submit feedback/blog/reflection
    # ...

def certificate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implement the logic to request a certificate for attended events
    # ...
'''


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Main
def main() -> None:
    # Set up the bot
    print('Starting Hack4GoodBOT...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("browse", browse_command))
    # dp.add_handler(CommandHandler("enroll", enroll))
    # dp.add_handler(CommandHandler("attended", attended))
    # dp.add_handler(CommandHandler("upcoming", upcoming))
    # dp.add_handler(CommandHandler("feedback", feedback))
    # dp.add_handler(CommandHandler("certificate", certificate))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()

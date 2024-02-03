import logging
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

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


# Commands
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Volunteer Chatbot! Type /help to see available commands.")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "/enroll - Enroll as a new volunteer\n"
        "/browse - Browse volunteering opportunities\n"
        "/attended - Check attended opportunities\n"
        "/upcoming - Check upcoming opportunities\n"
        "/feedback - Submit feedback/blog/reflection\n"
        "/certificate - Request a certificate for attended events"
    )

'''
def enroll(update: Update, context: CallbackContext) -> None:
    # Implement the logic to enroll as a new volunteer and save information to Google Sheets
    # ...
'''


def browse(update: Update, context: CallbackContext) -> None:
    # Access the sheet with volunteering opportunities
    sheet = client.open_by_key(SHEET_ID).worksheet(opportunities_sheet_name)

    # Fetch all records from the sheet
    opportunities = sheet.get_all_records()

    # Check if there are any opportunities listed
    if not opportunities:
        update.message.reply_text("Currently, there are no volunteering opportunities available.")
        return

    # Construct a message listing all opportunities
    message = "Here are the current volunteering opportunities available to join:\n\n"
    for idx, opportunity in enumerate(opportunities, start=1):
        # Assuming columns for 'Event Name', 'Date', 'Location', and 'Description'
        message += f"{idx}. {opportunity['Event Name']} - {opportunity['Date']} at {opportunity['Location']}\n" \
                   f"Description: {opportunity['Description']}\n\n"

    # Send the constructed message
    update.message.reply_text(message)


'''
def attended(update: Update, context: CallbackContext) -> None:
    # Implement the logic to check attended opportunities
    # ...

def upcoming(update: Update, context: CallbackContext) -> None:
    # Implement the logic to check upcoming opportunities
    # ...

def feedback(update: Update, context: CallbackContext) -> None:
    # Implement the logic to submit feedback/blog/reflection
    # ...

def certificate(update: Update, context: CallbackContext) -> None:
    # Implement the logic to request a certificate for attended events
    # ...
'''


def main() -> None:
    # Set up the bot
    print('Starting Hack4GoodBOT...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    #dp.add_handler(CommandHandler("enroll", enroll))
    app.add_handler(CommandHandler("browse", browse))
    #dp.add_handler(CommandHandler("attended", attended))
    #dp.add_handler(CommandHandler("upcoming", upcoming))
    #dp.add_handler(CommandHandler("feedback", feedback))
    #dp.add_handler(CommandHandler("certificate", certificate))

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval = 1)


if __name__ == '__main__':
    main()

import logging
from typing import Final

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext,
                          CallbackQueryHandler)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialization
TOKEN: Final = "6915448696:AAGa692f2FuuPsMzjhyw5b-Lllnc00g5f3M"
BOT_USERNAME: Final = "@Hack4GoodBOT"

# Google Sheets information
SHEET_ID: Final = "1dQOfj3kamyPNE5X0mO7YVlKtCP4awO_XX7B4Vhf9sZc"
opportunities_sheet_name = 'Opportunities'
register_sheet_name = 'Registrations'
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

    print(f'User ID: {update.message.from_user.id} ({update.message.chat.id}) in {message_type}: "{text}"')

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
    await update.message.reply_text("Hi there, I am Hack4GoodBOT!\nType /help to see available commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/enroll - Enroll as a new volunteer\n"
        "/browse - Browse volunteering opportunities\n"
        "/register - Check opportunities I have signed up\n"
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
    message = ("Here are the current volunteering opportunities available to join. "
               "Find out more at: https://www.bigatheart.org/ 🤩\n\n")
    for idx, opportunity in enumerate(opportunities, start=1):
        # Strip white spaces from each piece of text to avoid unexpected indentation
        message += (f"{idx}. Event: {opportunity['Event'].strip()}\n"
                    f"Location: {opportunity['Location'].strip()}\n"
                    f"Date: {opportunity['Date'].strip()}\n"
                    f"Time: {opportunity['Time'].strip()}\n"
                    f"Duration: {opportunity['Duration'].strip()}\n"
                    f"Participants Needed: {str(opportunity['Participants Needed']).strip()}\n"
                    f"Lunch Provided?: {opportunity['Lunch Provided?'].strip()}\n"
                    f"Description: {opportunity['Description'].strip()}\n"
                    f"Registration: {opportunity['Register'].strip()}\n\n")

    # Send the constructed message
    await update.message.reply_text(message)


async def register_command(update: Update, context: CallbackContext) -> None:
    # Access the sheet with volunteering opportunities
    events_sheet = client.open_by_key(SHEET_ID).worksheet(opportunities_sheet_name)
    events = events_sheet.get_all_records()

    # Create a list of InlineKeyboardButtons for each event
    buttons = [
        InlineKeyboardButton(text=event['Event'], callback_data=f"register_{event['Event']}")
        for event in events
    ]

    # Organize buttons into a keyboard layout
    keyboard = [buttons[i:i + 1] for i in range(0, len(buttons), 1)]  # one button per row
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with inline buttons
    await update.message.reply_text('Please choose an event to register:', reply_markup=reply_markup)


async def button_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Extract event name from the callback data
    event_name = query.data.split('_')[1]

    # Store the chosen event name in the user's context for later use
    context.user_data['chosen_event'] = event_name

    user_id = query.from_user.id

    # Access the 'Registrations' sheet
    registrations_sheet = client.open_by_key(SHEET_ID).worksheet(register_sheet_name)
    registrations = registrations_sheet.get_all_records()

    # Check if the user has already registered for the event
    already_registered = any(
        reg['Event'] == event_name and str(reg['User ID']) == str(user_id) for reg in registrations)

    if already_registered:
        # Inform the user that they are already registered
        await query.edit_message_text(text=f"You have already registered: {event_name}. "
                                           f"We appreciate your enthusiasm! 🤩"
                                           f"Thank you!")
    else:
        # Ask for registration confirmation
        keyboard = [
            InlineKeyboardButton(text="Yes", callback_data="confirm_registration"),
            InlineKeyboardButton(text="No", callback_data="cancel_registration")
        ]
        reply_markup = InlineKeyboardMarkup([keyboard])
        await query.edit_message_text(text=f"Confirm registration for {event_name}?", reply_markup=reply_markup)


async def confirmation_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if 'confirm_registration' in query.data:
        # Retrieve the chosen event name from the user's context
        event_name = context.user_data.get('chosen_event')
        events_sheet = client.open_by_key(SHEET_ID).worksheet('Opportunities')
        events = events_sheet.get_all_records()

        # Find the event details by the event name
        event_details = next((event for event in events if event['Event'] == event_name), None)
        if event_details:
            registration_url = event_details['Register']
            date_of_event = event_details['Date']
            user_id = query.from_user.id
            username = query.from_user.username  # Get the user's Telegram username

            # Access the 'Registrations' sheet
            registrations_sheet = client.open_by_key(SHEET_ID).worksheet(register_sheet_name)

            # Append the new registration
            # Include the username along with the other details
            registrations_sheet.append_row([event_name, date_of_event, user_id, username])

            # Provide the link to the Google Form for additional details
            await query.edit_message_text(text=f"You have been registered for {event_name}. "
                                               f"Please fill in the following form: {registration_url}")
        else:
            await query.edit_message_text(text="There was an error processing your registration. Please try again.")

    elif 'cancel_registration' in query.data:
        # User pressed "No", so we display the list of opportunities again
        await query.edit_message_reply_markup(reply_markup=await register_command(query, context))

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
    app.add_handler(CommandHandler("register", register_command))
    # dp.add_handler(CommandHandler("enroll", enroll))
    # dp.add_handler(CommandHandler("attended", attended))
    # dp.add_handler(CommandHandler("upcoming", upcoming))
    # dp.add_handler(CommandHandler("feedback", feedback))
    # dp.add_handler(CommandHandler("certificate", certificate))

    # Callback query handler for buttons
    app.add_handler(CallbackQueryHandler(button_callback_handler, pattern='^register_'))
    app.add_handler(
        CallbackQueryHandler(confirmation_callback_handler, pattern='^(confirm_registration|cancel_registration)$'))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()

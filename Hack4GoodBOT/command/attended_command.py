from Hack4GoodBOT.config import config
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackContext, CallbackQueryHandler)


# Attended Command
async def attended_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id  # Get the user's Telegram ID
    today = datetime.today().strftime('%d/%m/%Y')  # Today's date in the format used by your sheet

    # Access the 'Registrations' sheet
    registrations_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.register_sheet_name)
    registrations = registrations_sheet.get_all_records()

    # Filter registrations for events that have already occurred
    attended_events = [reg for reg in registrations if
                       str(reg['User ID']) == str(user_id) and datetime.strptime(reg['Date'],
                                                                                 '%d/%m/%Y') < datetime.strptime(today,
                                                                                                                 '%d/%m/%Y')]

    if not attended_events:
        await update.message.reply_text("You have not attended any events.")
        return

    # Construct a message listing all attended events
    message = "Here are the events you have attended:\n\n"
    for reg in attended_events:
        message += f"Event: {reg['Event']}\nDate: {reg['Date']}\n\n"

    await update.message.reply_text(message)

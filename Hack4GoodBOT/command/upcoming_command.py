from Hack4GoodBOT.config import config
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackContext, CallbackQueryHandler)


# Upcoming Command
async def upcoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id  # Get the user's Telegram ID
    today = datetime.today().strftime('%d/%m/%Y')  # Today's date in the format used by your sheet

    # Access the 'Registrations' sheet
    registrations_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.register_sheet_name)
    registrations = registrations_sheet.get_all_records()

    # Filter registrations for upcoming events
    upcoming_events = [reg for reg in registrations if
                       str(reg['User ID']) == str(user_id) and datetime.strptime(reg['Date'],
                                                                                 '%d/%m/%Y') >= datetime.strptime(today,
                                                                                                                  '%d/%m/%Y')]

    if not upcoming_events:
        await update.message.reply_text("You have no upcoming events.")
        return

    # Construct a message listing all upcoming events
    message = "Here are your upcoming events:\n\n"
    for reg in upcoming_events:
        message += f"Event: {reg['Event']}\nDate: {reg['Date']}\n\n"

    await update.message.reply_text(message)

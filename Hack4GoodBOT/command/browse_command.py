from Hack4GoodBOT.config import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackContext, CallbackQueryHandler)


# Browse Command
async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Access the sheet with volunteering opportunities
    sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.opportunities_sheet_name)

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

from telegram import Update
from telegram.ext import (ContextTypes)


# Start Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi there, I am Hack4GoodBOT!\nType /help to see available commands.")
